import 'package:http/http.dart' as http;

class TflApiService {
  Future<String> getArrivalsForStation(
      String busLineId, String stopPointId) async {
    final response = await http.get(Uri.parse(
        'https://api.tfl.gov.uk/Line/$busLineId/Arrivals/$stopPointId'));

    if (response.statusCode == 200) {
      return response.body;
    } else {
      throw Exception('Failed to load arrival predictions');
    }
  }
}