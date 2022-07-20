import 'dart:async';

import 'package:active_delay_app/location_handler.dart';
import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:location/location.dart';

class GoogleMaps extends StatefulWidget {
  const GoogleMaps({Key? key}) : super(key: key);

  @override
  State<GoogleMaps> createState() => _MapState();
}

class _MapState extends State<GoogleMaps> {
  final Completer<GoogleMapController> _controller = Completer();

  final LocationHandler _locationHandler = LocationHandler();

  static const CameraPosition _kGooglePlex = CameraPosition(
    target: LatLng(37.42796133580664, -122.085749655962),
    zoom: 14.4746,
  );

  @override
  Widget build(BuildContext context) {
    return GoogleMap(
      mapType: MapType.normal,
      initialCameraPosition: _kGooglePlex,
      onMapCreated: (GoogleMapController controller) async {
        final LocationData? location = await _locationHandler.getLocation();
        controller.animateCamera(CameraUpdate.newCameraPosition(CameraPosition(
            target: LatLng(location!.latitude!, location.longitude!))));
        _controller.complete(controller);
      },
      myLocationEnabled: true,
      myLocationButtonEnabled: true,
    );
  }
}
