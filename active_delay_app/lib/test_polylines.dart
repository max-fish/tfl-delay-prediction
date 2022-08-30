import 'dart:io';
import 'package:path/path.dart' as p;
import 'dart:convert';

void main(List<String> args) {
  Future<void> getRoute() async {
    final filePath = p.join(Directory.current.path, 'polylines-453.txt');

    File file = File(filePath);

    final String string = await file.readAsString();

    List coordinatesJson = json.decode(string);

    List<List<double>> coordinatesList = coordinatesJson
        .map((polyline) =>
            [polyline.elementAt(0) as double, polyline.elementAt(1) as double])
        .toList();

    print(coordinatesList);
    // Iterable<Match> polylines = string.allMatches(r'');

    // polylines.toList();

    // print(polylines);
  }

  getRoute();
}
