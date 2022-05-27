// const { mongodb } = require('./mongo_db_setup');

$.connection.hub.logging = true;
$.connection.hub.url = "https://push-api.tfl.gov.uk/signalr/hubs/signalr";

var hub = $.connection.predictionsRoomHub;


jQuery(document).on('click', '#connectButton', () => {
  console.log('start');

  hub.client.showPredictions = printBoard;

  $.connection.hub.start().done(function() {
  console.log("tfl.predictions: connection started");
  var lineRooms = [{"LineId": "1"}, {"LineId": "100"}, {"LineId": "101"}, {"LineId": "102"}, {"LineId": "103"}, {"LineId": "104"}, {"LineId": "105"}, {"LineId": "106"}, {"LineId": "107"}, {"LineId": "108"}, {"LineId": "109"}, {"LineId": "11"}, {"LineId": "110"}, {"LineId": "111"}, {"LineId": "112"}, {"LineId": "113"}, {"LineId": "114"}, {"LineId": "115"}, {"LineId": "116"}, {"LineId": "117"}, {"LineId": "118"}, {"LineId": "119"}, {"LineId": "12"}, {"LineId": "120"}, {"LineId": "121"}, {"LineId": "122"}, {"LineId": "123"}, {"LineId": "124"}, {"LineId": "125"}, {"LineId": "126"}, {"LineId": "127"}, {"LineId": "128"}, {"LineId": "129"}, {"LineId": "13"}, {"LineId": "130"}, {"LineId": "131"}, {"LineId": "132"}, {"LineId": "133"}, {"LineId": "134"}, {"LineId": "135"}, {"LineId": "136"}, {"LineId": "137"}, {"LineId": "138"}, {"LineId": "139"}, {"LineId": "14"}, {"LineId": "140"}, {"LineId": "141"}, {"LineId": "142"}, {"LineId": "143"}, {"LineId": "144"}, {"LineId": "145"}, {"LineId": "146"}, {"LineId": "147"}, {"LineId": "148"}, {"LineId": "149"}, {"LineId": "15"}, {"LineId": "150"}, {"LineId": "151"}, {"LineId": "152"}, {"LineId": "153"}, {"LineId": "154"}, {"LineId": "155"}, {"LineId": "156"}, {"LineId": "157"}, {"LineId": "158"}, {"LineId": "159"}, {"LineId": "16"}, {"LineId": "160"}, {"LineId": "161"}, {"LineId": "162"}, {"LineId": "163"}, {"LineId": "164"}, {"LineId": "165"}, {"LineId": "166"}, {"LineId": "167"}, {"LineId": "168"}, {"LineId": "169"}, {"LineId": "17"}, {"LineId": "170"}, {"LineId": "171"}, {"LineId": "172"}, {"LineId": "173"}, {"LineId": "174"}, {"LineId": "175"}, {"LineId": "176"}, {"LineId": "177"}, {"LineId": "178"}, {"LineId": "179"}, {"LineId": "18"}, {"LineId": "180"}, {"LineId": "181"}, {"LineId": "182"}, {"LineId": "183"}, {"LineId": "184"}, {"LineId": "185"}, {"LineId": "186"}, {"LineId": "187"}, {"LineId": "188"}, {"LineId": "189"}, {"LineId": "19"}, {"LineId": "190"}, {"LineId": "191"}, {"LineId": "192"}, {"LineId": "193"}, {"LineId": "194"}, {"LineId": "195"}, {"LineId": "196"}, {"LineId": "197"}, {"LineId": "198"}, {"LineId": "199"}, {"LineId": "2"}, {"LineId": "20"}, {"LineId": "200"}, {"LineId": "201"}, {"LineId": "202"}, {"LineId": "203"}, {"LineId": "204"}, {"LineId": "205"}, {"LineId": "206"}, {"LineId": "207"}, {"LineId": "208"}, {"LineId": "209"}, {"LineId": "21"}, {"LineId": "210"}, {"LineId": "211"}, {"LineId": "212"}, {"LineId": "213"}, {"LineId": "214"}, {"LineId": "215"}, {"LineId": "216"}, {"LineId": "217"}, {"LineId": "218"}, {"LineId": "219"}, {"LineId": "22"}, {"LineId": "220"}, {"LineId": "221"}, {"LineId": "222"}, {"LineId": "223"}, {"LineId": "224"}, {"LineId": "225"}, {"LineId": "226"}, {"LineId": "227"}, {"LineId": "228"}, {"LineId": "229"}, {"LineId": "23"}, {"LineId": "230"}, {"LineId": "231"}, {"LineId": "232"}, {"LineId": "233"}, {"LineId": "234"}, {"LineId": "235"}, {"LineId": "236"}, {"LineId": "237"}, {"LineId": "238"}, {"LineId": "24"}, {"LineId": "240"}, {"LineId": "241"}, {"LineId": "242"}, {"LineId": "243"}, {"LineId": "244"}, {"LineId": "245"}, {"LineId": "246"}, {"LineId": "247"}, {"LineId": "248"}, {"LineId": "249"}, {"LineId": "25"}, {"LineId": "250"}, {"LineId": "251"}, {"LineId": "252"}, {"LineId": "253"}, {"LineId": "254"}, {"LineId": "255"}, {"LineId": "256"}, {"LineId": "257"}, {"LineId": "258"}, {"LineId": "259"}, {"LineId": "26"}, {"LineId": "260"}, {"LineId": "261"}, {"LineId": "262"}, {"LineId": "263"}, {"LineId": "264"}, {"LineId": "265"}, {"LineId": "266"}, {"LineId": "267"}, {"LineId": "268"}, {"LineId": "269"}, {"LineId": "27"}, {"LineId": "270"}, {"LineId": "271"}, {"LineId": "272"}, {"LineId": "273"}, {"LineId": "274"}, {"LineId": "275"}, {"LineId": "276"}, {"LineId": "277"}, {"LineId": "278"}, {"LineId": "279"}, {"LineId": "28"}, {"LineId": "280"}, {"LineId": "281"}, {"LineId": "282"}, {"LineId": "283"}, {"LineId": "284"}, {"LineId": "285"}, {"LineId": "286"}, {"LineId": "287"}, {"LineId": "288"}, {"LineId": "289"}, {"LineId": "29"}, {"LineId": "290"}, {"LineId": "291"}, {"LineId": "292"}, {"LineId": "293"}, {"LineId": "294"}, {"LineId": "295"}, {"LineId": "296"}, {"LineId": "297"}, {"LineId": "298"}, {"LineId": "299"}, {"LineId": "3"}, {"LineId": "30"}, {"LineId": "300"}, {"LineId": "301"}, {"LineId": "302"}, {"LineId": "303"}, {"LineId": "304"}, {"LineId": "306"}, {"LineId": "307"}, {"LineId": "308"}, {"LineId": "309"}, {"LineId": "31"}, {"LineId": "312"}, {"LineId": "313"}, {"LineId": "314"}, {"LineId": "315"}, {"LineId": "316"}, {"LineId": "317"}, {"LineId": "318"}, {"LineId": "319"}, {"LineId": "32"}, {"LineId": "320"}, {"LineId": "321"}, {"LineId": "322"}, {"LineId": "323"}, {"LineId": "324"}, {"LineId": "325"}, {"LineId": "326"}, {"LineId": "327"}, {"LineId": "328"}, {"LineId": "329"}, {"LineId": "33"}, {"LineId": "330"}, {"LineId": "331"}, {"LineId": "332"}, {"LineId": "333"}, {"LineId": "335"}, {"LineId": "336"}, {"LineId": "337"}, {"LineId": "339"}, {"LineId": "34"}, {"LineId": "340"}, {"LineId": "341"}, {"LineId": "343"}, {"LineId": "344"}, {"LineId": "345"}, {"LineId": "346"}, {"LineId": "347"}, {"LineId": "349"}, {"LineId": "35"}, {"LineId": "350"}, {"LineId": "352"}, {"LineId": "353"}, {"LineId": "354"}, {"LineId": "355"}, {"LineId": "356"}, {"LineId": "357"}, {"LineId": "358"}, {"LineId": "359"}, {"LineId": "36"}, {"LineId": "360"}, {"LineId": "362"}, {"LineId": "363"}, {"LineId": "364"}, {"LineId": "365"}, {"LineId": "366"}, {"LineId": "367"}, {"LineId": "368"}, {"LineId": "37"}, {"LineId": "370"}, {"LineId": "371"}, {"LineId": "372"}, {"LineId": "375"}, {"LineId": "376"}, {"LineId": "377"}, {"LineId": "378"}, {"LineId": "379"}, {"LineId": "38"}, {"LineId": "380"}, {"LineId": "381"}, {"LineId": "382"}, {"LineId": "383"}, {"LineId": "384"}, {"LineId": "385"}, {"LineId": "386"}, {"LineId": "388"}, {"LineId": "389"}, {"LineId": "39"}, {"LineId": "390"}, {"LineId": "393"}, {"LineId": "394"}, {"LineId": "395"}, {"LineId": "396"}, {"LineId": "397"}, {"LineId": "398"}, {"LineId": "399"}, {"LineId": "4"}, {"LineId": "40"}, {"LineId": "401"}, {"LineId": "403"}, {"LineId": "404"}, {"LineId": "405"}, {"LineId": "406"}, {"LineId": "407"}, {"LineId": "41"}, {"LineId": "410"}, {"LineId": "411"}, {"LineId": "412"}, {"LineId": "413"}, {"LineId": "414"}, {"LineId": "415"}, {"LineId": "417"}, {"LineId": "418"}, {"LineId": "419"}, {"LineId": "42"}, {"LineId": "422"}, {"LineId": "423"}, {"LineId": "424"}, {"LineId": "425"}, {"LineId": "427"}, {"LineId": "428"}, {"LineId": "43"}, {"LineId": "430"}, {"LineId": "432"}, {"LineId": "433"}, {"LineId": "434"}, {"LineId": "436"}, {"LineId": "44"}, {"LineId": "440"}, {"LineId": "444"}, {"LineId": "45"}, {"LineId": "450"}, {"LineId": "452"}, {"LineId": "453"}, {"LineId": "455"}, {"LineId": "456"}, {"LineId": "46"}, {"LineId": "460"}, {"LineId": "462"}, {"LineId": "463"}, {"LineId": "464"}, {"LineId": "465"}, {"LineId": "466"}, {"LineId": "467"}, {"LineId": "468"}, {"LineId": "469"}, {"LineId": "47"}, {"LineId": "470"}, {"LineId": "472"}, {"LineId": "473"}, {"LineId": "474"}, {"LineId": "476"}, {"LineId": "481"}, {"LineId": "482"}, {"LineId": "483"}, {"LineId": "484"}, {"LineId": "485"}, {"LineId": "486"}, {"LineId": "487"}, {"LineId": "488"}, {"LineId": "49"}, {"LineId": "490"}, {"LineId": "491"}, {"LineId": "492"}, {"LineId": "493"}, {"LineId": "496"}, {"LineId": "497"}, {"LineId": "498"}, {"LineId": "499"}, {"LineId": "5"}, {"LineId": "50"}, {"LineId": "507"}, {"LineId": "51"}, {"LineId": "52"}, {"LineId": "521"}, {"LineId": "53"}, {"LineId": "533"}, {"LineId": "54"}, {"LineId": "549"}, {"LineId": "55"}, {"LineId": "56"}, {"LineId": "57"}, {"LineId": "58"}, {"LineId": "59"}, {"LineId": "6"}, {"LineId": "60"}, {"LineId": "601"}, {"LineId": "602"}, {"LineId": "603"}, {"LineId": "605"}, {"LineId": "606"}, {"LineId": "607"}, {"LineId": "608"}, {"LineId": "61"}, {"LineId": "612"}, {"LineId": "613"}, {"LineId": "616"}, {"LineId": "617"}, {"LineId": "62"}, {"LineId": "621"}, {"LineId": "624"}, {"LineId": "625"}, {"LineId": "626"}, {"LineId": "627"}, {"LineId": "628"}, {"LineId": "629"}, {"LineId": "63"}, {"LineId": "631"}, {"LineId": "632"}, {"LineId": "633"}, {"LineId": "634"}, {"LineId": "635"}, {"LineId": "638"}, {"LineId": "639"}, {"LineId": "64"}, {"LineId": "640"}, {"LineId": "642"}, {"LineId": "643"}, {"LineId": "645"}, {"LineId": "646"}, {"LineId": "649"}, {"LineId": "65"}, {"LineId": "650"}, {"LineId": "651"}, {"LineId": "652"}, {"LineId": "653"}, {"LineId": "654"}, {"LineId": "655"}, {"LineId": "656"}, {"LineId": "657"}, {"LineId": "658"}, {"LineId": "66"}, {"LineId": "660"}, {"LineId": "661"}, {"LineId": "662"}, {"LineId": "663"}, {"LineId": "664"}, {"LineId": "665"}, {"LineId": "669"}, {"LineId": "67"}, {"LineId": "670"}, {"LineId": "671"}, {"LineId": "672"}, {"LineId": "673"}, {"LineId": "674"}, {"LineId": "675"}, {"LineId": "677"}, {"LineId": "678"}, {"LineId": "679"}, {"LineId": "68"}, {"LineId": "681"}, {"LineId": "683"}, {"LineId": "684"}, {"LineId": "685"}, {"LineId": "686"}, {"LineId": "687"}, {"LineId": "688"}, {"LineId": "689"}, {"LineId": "69"}, {"LineId": "690"}, {"LineId": "692"}, {"LineId": "696"}, {"LineId": "697"}, {"LineId": "698"}, {"LineId": "699"}, {"LineId": "7"}, {"LineId": "70"}, {"LineId": "71"}, {"LineId": "72"}, {"LineId": "73"}, {"LineId": "74"}, {"LineId": "75"}, {"LineId": "76"}, {"LineId": "77"}, {"LineId": "78"}, {"LineId": "79"}, {"LineId": "8"}, {"LineId": "80"}, {"LineId": "81"}, {"LineId": "83"}, {"LineId": "85"}, {"LineId": "86"}, {"LineId": "87"}, {"LineId": "88"}, {"LineId": "89"}, {"LineId": "9"}, {"LineId": "90"}, {"LineId": "91"}, {"LineId": "92"}, {"LineId": "93"}, {"LineId": "94"}, {"LineId": "95"}, {"LineId": "96"}, {"LineId": "969"}, {"LineId": "97"}, {"LineId": "98"}, {"LineId": "99"}, {"LineId": "A10"}, {"LineId": "B11"}, {"LineId": "B12"}, {"LineId": "B13"}, {"LineId": "B14"}, {"LineId": "B15"}, {"LineId": "B16"}, {"LineId": "C1"}, {"LineId": "C10"}, {"LineId": "C11"}, {"LineId": "C3"}, {"LineId": "D3"}, {"LineId": "D6"}, {"LineId": "D7"}, {"LineId": "D8"}, {"LineId": "E1"}, {"LineId": "E10"}, {"LineId": "E11"}, {"LineId": "E2"}, {"LineId": "E3"}, {"LineId": "E5"}, {"LineId": "E6"}, {"LineId": "E7"}, {"LineId": "E8"}, {"LineId": "E9"}, {"LineId": "EL1"}, {"LineId": "EL2"}, {"LineId": "EL3"}, {"LineId": "G1"}, {"LineId": "H10"}, {"LineId": "H11"}, {"LineId": "H12"}, {"LineId": "H13"}, {"LineId": "H14"}, {"LineId": "H17"}, {"LineId": "H18"}, {"LineId": "H19"}, {"LineId": "H2"}, {"LineId": "H20"}, {"LineId": "H22"}, {"LineId": "H25"}, {"LineId": "H26"}, {"LineId": "H28"}, {"LineId": "H3"}, {"LineId": "H32"}, {"LineId": "H37"}, {"LineId": "H9"}, {"LineId": "H91"}, {"LineId": "H98"}, {"LineId": "K1"}, {"LineId": "K2"}, {"LineId": "K3"}, {"LineId": "K4"}, {"LineId": "K5"}, {"LineId": "N1"}, {"LineId": "N109"}, {"LineId": "N11"}, {"LineId": "N113"}, {"LineId": "N133"}, {"LineId": "N136"}, {"LineId": "N140"}, {"LineId": "N15"}, {"LineId": "N155"}, {"LineId": "N16"}, {"LineId": "N171"}, {"LineId": "N18"}, {"LineId": "N19"}, {"LineId": "N199"}, {"LineId": "N2"}, {"LineId": "N20"}, {"LineId": "N205"}, {"LineId": "N207"}, {"LineId": "N21"}, {"LineId": "N22"}, {"LineId": "N242"}, {"LineId": "N25"}, {"LineId": "N250"}, {"LineId": "N253"}, {"LineId": "N26"}, {"LineId": "N266"}, {"LineId": "N27"}, {"LineId": "N277"}, {"LineId": "N279"}, {"LineId": "N28"}, {"LineId": "N29"}, {"LineId": "N3"}, {"LineId": "N31"}, {"LineId": "N33"}, {"LineId": "N343"}, {"LineId": "N38"}, {"LineId": "N381"}, {"LineId": "N41"}, {"LineId": "N44"}, {"LineId": "N5"}, {"LineId": "N53"}, {"LineId": "N55"}, {"LineId": "N550"}, {"LineId": "N551"}, {"LineId": "N63"}, {"LineId": "N65"}, {"LineId": "N68"}, {"LineId": "N7"}, {"LineId": "N72"}, {"LineId": "N73"}, {"LineId": "N74"}, {"LineId": "N8"}, {"LineId": "N83"}, {"LineId": "N86"}, {"LineId": "N87"}, {"LineId": "N89"}, {"LineId": "N9"}, {"LineId": "N91"}, {"LineId": "N97"}, {"LineId": "N98"}, {"LineId": "P12"}, {"LineId": "P13"}, {"LineId": "P4"}, {"LineId": "P5"}, {"LineId": "R1"}, {"LineId": "R10"}, {"LineId": "R11"}, {"LineId": "R2"}, {"LineId": "R3"}, {"LineId": "R4"}, {"LineId": "R5"}, {"LineId": "R6"}, {"LineId": "R68"}, {"LineId": "R7"}, {"LineId": "R70"}, {"LineId": "R8"}, {"LineId": "R9"}, {"LineId": "S1"}, {"LineId": "S3"}, {"LineId": "S4"}, {"LineId": "U1"}, {"LineId": "U10"}, {"LineId": "U2"}, {"LineId": "U3"}, {"LineId": "U4"}, {"LineId": "U5"}, {"LineId": "U7"}, {"LineId": "U9"}, {"LineId": "W11"}, {"LineId": "W12"}, {"LineId": "W13"}, {"LineId": "W14"}, {"LineId": "W15"}, {"LineId": "W16"}, {"LineId": "W19"}, {"LineId": "W3"}, {"LineId": "W4"}, {"LineId": "W5"}, {"LineId": "W6"}, {"LineId": "W7"}, {"LineId": "W8"}, {"LineId": "W9"}, {"LineId": "X140"}, {"LineId": "X26"}, {"LineId": "X68"}];

hub.server.addLineRooms(lineRooms)
          .done(function () {
             console.log("tfl.predictions: Invocation of addLineRooms succeeded");
             return;
          })
         .fail(function (error) {
             console.log("tfl.predictions: Invocation of addLineRooms failed. Error: " + error);
             return;
         });
});
});

jQuery(document).on('click', '#disconnectButton', () => {
  console.log('stop');
  hub.client.showPredictions = null;
  $.connection.hub.stop(true, true);
  clearInterval(checkTimeout);
  // mongodb.closeDatabaseConnection();
});

// function updateBoard(data) {
//             $("#board").empty();
//             data.sort(sortByTts);
  
//             $.each(data, function( index, prediction ) {
//               var mins = Math.floor(prediction.TimeToStation/60);
//               var due = mins === 0 ? "Due" : mins + "m"; 
//                 $("#board").append("<tr><td>" + prediction.Towards + "</td><td>" + due + "</td><td>" + prediction.CurrentLocation + "</td></tr>");
//             });
    
//             console.log(data);
//             return true;
// };

var predictions = []

var locked = false;

var checkTimeout = setInterval(function() {
  if(predictions.length !== 0) {
    sendToDjango();
  }
}, 1000)

function printBoard(data) {
  predictions.push(...data);
  // console.log(data);
}

function sendToDjango() {

    fetch('http://127.0.0.1:8000/api/', {
      method: 'POST',
      mode: 'no-cors',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(predictions)
    }).then(() => {
      console.log(predictions.length);
      predictions = [];
      console.log('Sent successfully');
    })
    .catch((error) => {
        console.error('error: ' + error);
      });
}



function until(conditionFunction) {

  const poll = resolve => {
    if(conditionFunction()) resolve();
    else setTimeout(_ => poll(resolve), 400);
  }

  return new Promise(poll);
}

function sortByTts(a, b) {
  return ((a.TimeToStation < b.TimeToStation) ? -1 : ((a.TimeToStation > b.TimeToStation) ? 1 : 0));
};