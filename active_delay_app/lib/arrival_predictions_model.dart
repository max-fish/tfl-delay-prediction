class ArrivalPrediction {
  final String destinationName;
  final String direction;
  final int timeToStation;
  final String expectedArrival;
  final String timeOfPrediction;
  int? predictedArrival;
  int? lowEnd;
  int? highEnd;

  ArrivalPrediction(
      {required this.destinationName,
      required this.direction,
      required this.timeToStation,
      required this.expectedArrival,
      required this.timeOfPrediction,
      this.predictedArrival,
      this.lowEnd,
      this.highEnd});

  factory ArrivalPrediction.fromJson(Map<String, dynamic> json) {
    return ArrivalPrediction(
        destinationName: json['destinationName'],
        direction: json['direction'],
        timeToStation: json['timeToStation'],
        expectedArrival: json['expectedArrival'],
        timeOfPrediction: json['timestamp']);
  }

  void setPredictedArrival(int predictedArrival) {
    this.predictedArrival = predictedArrival;
  }

  void setLowEnd(int lowEnd) {
    this.lowEnd = lowEnd;
  }

  void setHighEnd(int highEnd) {
    this.highEnd = highEnd;
  }
}
