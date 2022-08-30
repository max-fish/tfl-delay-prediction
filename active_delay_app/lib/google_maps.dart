import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';

import 'package:active_delay_app/arrival_predictions_model.dart';
import 'package:active_delay_app/location_handler.dart';
import 'package:active_delay_app/tfl_api_service.dart';
import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:location/location.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'dart:ui' as ui;

class GoogleMaps extends StatefulWidget {
  const GoogleMaps({Key? key}) : super(key: key);

  @override
  State<GoogleMaps> createState() => _MapState();
}

class _MapState extends State<GoogleMaps> {
  final Completer<GoogleMapController> _controller = Completer();

  final LocationHandler _locationHandler = LocationHandler();

  static const CameraPosition _kGooglePlex = CameraPosition(
    target: LatLng(51.5072, 0.1276),
    zoom: 14.4746,
  );

  final Set<Marker> _markers = {};
  final Set<Polyline> _polylines = {};

//credit to: https://flutterhq.com/questions-and-answers/231/how-to-change-the-icon-size-of-google-maps-marker-in-flutter
  Future<BitmapDescriptor> getMarkerIcon() async {
    ByteData data = await rootBundle.load('assets/marker_icon.png');
    ui.Codec codec = await ui.instantiateImageCodec(data.buffer.asUint8List(),
        targetWidth: 20);
    ui.FrameInfo fi = await codec.getNextFrame();
    Uint8List markerIconInBytes =
        (await fi.image.toByteData(format: ui.ImageByteFormat.png))!
            .buffer
            .asUint8List();

    return BitmapDescriptor.fromBytes(markerIconInBytes);

    // BitmapDescriptor icon = await BitmapDescriptor.fromAssetImage(
    //     ImageConfiguration(size: Size(0.1, 0.1)), 'assets/marker_icon.png');
  }

  Future<void> plotRoute() async {
    final String string =
        await rootBundle.loadString('assets/polylines_208.txt');

    List coordinatesJson = json.decode(string);

    List<LatLng> coordinatesList = coordinatesJson
        .map((coordinate) => LatLng(coordinate.elementAt(1) as double,
            coordinate.elementAt(0) as double))
        .toList();

    setState(() {
      _polylines.add(Polyline(
          polylineId: const PolylineId('453'),
          points: coordinatesList,
          visible: true,
          width: 4,
          color: Colors.red));
    });
  }

  Future<void> plotStations() async {
    final String stationsString =
        await rootBundle.loadString('assets/stations_208_outbound.txt');

    final List stationsList = json.decode(stationsString);

    final String modelString =
        await rootBundle.loadString('assets/model_data_208_outbound.json');

    final modelData = json.decode(modelString);

    BitmapDescriptor icon = await getMarkerIcon();

    Iterable<Marker> markers = stationsList.map((station) => Marker(
          markerId: MarkerId(station['id']),
          position: LatLng(station['lat'], station['lon']),
          icon: icon,
          onTap: () {
            TflApiService tflApiService = TflApiService();
            Scaffold.of(context).showBottomSheet((context) {
              return Padding(
                padding: const EdgeInsets.all(8.0),
                child: Container(
                  height: 250,
                  decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(20)),
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Center(
                      child: FutureBuilder(
                          future: tflApiService.getArrivalsForStation(
                              '208', station['id']),
                          builder: (context, AsyncSnapshot<String> snapshot) {
                            if (snapshot.hasData) {
                              final DateTime currentDateTime = DateTime.now();

                              final List arrivalPredictionsJson =
                                  json.decode(snapshot.data!);

                              final List<ArrivalPrediction> arrivalPredictions =
                                  arrivalPredictionsJson
                                      .map((arrivalPrediction) {
                                ArrivalPrediction arrivalPredictionObject =
                                    ArrivalPrediction.fromJson(
                                        arrivalPrediction);

                                String timeOfPrediction =
                                    arrivalPredictionObject.timeOfPrediction;

                                DateTime dateTime =
                                    DateTime.parse(timeOfPrediction).toLocal();

                                bool isWeekend = dateTime.weekday >= 6;

                                int timeToStation =
                                    arrivalPredictionObject.timeToStation;

                                int timetoStationSection =
                                    (timeToStation / 1790).floor() + 1;

                                final errorData = modelData[
                                    '${isWeekend}_$timetoStationSection'];

                                DateTime expectedArrival = DateTime.parse(
                                        arrivalPredictionObject.expectedArrival)
                                    .toLocal();

                                DateTime predictedArrival = expectedArrival.add(
                                    Duration(
                                        minutes: errorData['error'].round()));

                                DateTime lowEnd = expectedArrival.add(Duration(
                                    minutes: errorData['low_end'].round()));

                                DateTime highEnd = expectedArrival.add(Duration(
                                    minutes: errorData['high_end'].round()));

                                final int predictedArrivalInMinutes =
                                    predictedArrival
                                        .difference(currentDateTime)
                                        .inMinutes;

                                final int lowEndInMinutes = lowEnd
                                    .difference(currentDateTime)
                                    .inMinutes;

                                final int highEndInMinutes = highEnd
                                    .difference(currentDateTime)
                                    .inMinutes;

                                arrivalPredictionObject.setPredictedArrival(
                                    predictedArrivalInMinutes);

                                arrivalPredictionObject
                                    .setLowEnd(lowEndInMinutes);

                                arrivalPredictionObject
                                    .setHighEnd(highEndInMinutes);

                                return arrivalPredictionObject;
                              }).toList();

                              arrivalPredictions.sort(((a, b) =>
                                  a.timeToStation.compareTo(b.timeToStation)));

                              return Column(
                                children: [
                                  Align(alignment: Alignment.centerLeft,child: Text(station['name'], style: Theme.of(context).textTheme.headlineSmall!.copyWith(color: Theme.of(context).textTheme.headlineMedium!.color),),),
                                  ListView.separated(
                                      shrinkWrap: true,
                                      itemCount: arrivalPredictions.length,
                                      separatorBuilder: (context, index) => const Divider(),
                                      itemBuilder: (context, index) {
                                        final ArrivalPrediction arrivalPrediction =
                                            arrivalPredictions.elementAt(index);
                                        return ListTile(
                                          title: Text(
                                              arrivalPrediction.destinationName),
                                          subtitle: RichText(
                                            text: TextSpan(
                                              style: Theme.of(context).textTheme.headline6,
                                              children: [
                                                TextSpan(text: '${arrivalPrediction.lowEnd.toString()} min', style: Theme.of(context).textTheme.headline6!.copyWith(color: Colors.green)),
                                                TextSpan(text: '--'),
                                                TextSpan(text: '${arrivalPrediction.highEnd.toString()} min', style: Theme.of(context).textTheme.headline6!.copyWith(color: Colors.red))
                                                ])),
                                          trailing: Text(arrivalPrediction.predictedArrival.toString(), style: Theme.of(context).textTheme.headline6,),
                                        );
                                      }),
                                ],
                              );
                            } else if (snapshot.hasError) {
                              return const Text('Could not load data :(');
                            } else {
                              return const CircularProgressIndicator();
                            }
                          }),
                    ),
                  ),
                ),
              );
            }, backgroundColor: Colors.transparent);
          },
        ));

    setState(() {
      _markers.addAll(markers);
    });
  }

  @override
  Widget build(BuildContext context) {
    return GoogleMap(
      mapType: MapType.normal,
      initialCameraPosition: _kGooglePlex,
      onMapCreated: (GoogleMapController controller) async {
        final LocationData? location = await _locationHandler.getLocation();
        await controller.animateCamera(CameraUpdate.newCameraPosition(
            CameraPosition(
                target: LatLng(location!.latitude!, location.longitude!),
                zoom: 14)));
        await plotRoute();
        await plotStations();
        _controller.complete(controller);
      },
      myLocationEnabled: true,
      myLocationButtonEnabled: true,
      markers: _markers,
      polylines: _polylines,
    );
  }
}
