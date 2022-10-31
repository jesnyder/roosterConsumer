
var calculatePassages = function functioncalculatePassages(inputInfo){

  var passages = inputInfo.passages;

  var mediaTotal = 0;
  var trypleTotal = 0;
  var flaskDesc = '';

  for (let i=inputInfo.passages; i>0; i--) {

    if (i < inputInfo.passages){
      inputInfo.cellEstimate =  inputInfo.last.cellSeed;
    };

    var Pfound = Pchars(inputInfo, i);
    inputInfo.last = Pfound;

    mediaTotal = mediaTotal + Pfound.mediaTotal;
    inputInfo.mediaTotal = mediaTotal;
    trypleTotal = trypleTotal + Pfound.trypleTotal;
    inputInfo.trypleTotal = trypleTotal;
    inputInfo.mediaBottles = Math.ceil(mediaTotal/500);
    flaskDesc = flaskDesc + ' ' + Pfound.flaskType + ' x' + Pfound.flaskCount;
    if (i > 1){
      flaskDesc = flaskDesc + ' + '
    };
    inputInfo.flaskDesc = flaskDesc;
    inputInfo.flaskDescLong =  Math.ceil(mediaTotal/500) + ' bottles RoosterNourish + ' + flaskDesc;
    inputInfo.mediaDescLong =  Math.ceil(mediaTotal/500) + ' bottles RoosterNourish';

    if (inputInfo.passage == inputInfo.passages){
      inputInfo.cellYieldTotal = Pfound.cellYield;
      inputInfo.cellYieldTotalReadable = (Pfound.cellYield).toLocaleString('en-US');
      inputInfo.overfill = Math.round(Pfound.cellYield/inputInfo.cells*100-100);
      inputInfo.EVCollect =  Pfound.mediaPer * Pfound.flaskCount;
    };
    if (inputInfo.passage == 1){
      inputInfo.cellSeedTotal = Pfound.cellSeed;
      inputInfo.cellSeedTotalReadable = (Pfound.cellSeed).toLocaleString('en-US');
      inputInfo.RoosterGem = Pfound.mediaPer * Pfound.flaskCount;
    };

    if (inputInfo.passage == 1){
      inputInfo.P1 = Pfound;
    };
    if (inputInfo.passage == 2){
      inputInfo.P2 = Pfound;
    };
    if (inputInfo.passage == 3){
      inputInfo.P3 = Pfound;
    };
    if (inputInfo.passage == 4){
      inputInfo.P4 = Pfound;
    };
    if (inputInfo.passage == 5){
      inputInfo.P5 = Pfound;
    };

    console.log('inputInfo.passage = ')
    console.log(inputInfo.passage)
    console.log('inputInfo = ')
    console.log(inputInfo)

  };

  return(inputInfo)
  };


var Pchars = function functionPchars(inputInfo, i){

  inputInfo.passage = i;

  if (i = inputInfo.passages){
    var cellEstimate = inputInfo.cellEstimate;
  }
  else {
    var cellEstimate = inputInfo.last.cellSeed;
    console.log('cellEstimate = ')
    console.log(cellsEstimate)
  };

  var flaskCountLowest = 10**100;

  for (let j = 0; j<flaskNames.length; j++) {

    var flaskName = flaskNames[j];
    var flasks = cellEstimate / (flaskVars(flaskName).surArea * inputInfo.confluentDensity);

    if (flasks >= 0.75){

      if (flasks < flaskCountLowest){

        flasks = Math.ceil(flasks);

        if (flaskName == 'CS5' && flasks/2>0 && flasks%2 == 0){
          flaskName = 'CS10';
          flasks = flasks/2;
        };

        flaskCountLowest = flasks;

        var mediaVolume = flasks*(flaskVars(flaskName).mediaVol + flaskVars(flaskName).trypleVol);

        var returnVar = {
          passage: inputInfo.passage,
          flaskType: flaskName,
          flaskCount: flasks,
          cellSeed: flaskVars(flaskName).surArea * inputInfo.density * flasks,
          cellYield: flaskVars(flaskName).surArea * inputInfo.confluentDensity * flasks,
          cellSeedReadable: (flaskVars(flaskName).surArea * inputInfo.density * flasks).toLocaleString('en-US'),
          cellYieldReadable: (flaskVars(flaskName).surArea * inputInfo.confluentDensity * flasks).toLocaleString('en-US'),
          mediaTotal: mediaVolume,
          trypleTotal: flaskVars(flaskName).trypleVol * flasks,
          cellSeedPer: flaskVars(flaskName).surArea * inputInfo.density,
          cellYieldPer: flaskVars(flaskName).surArea * inputInfo.confluentDensity,
          cellSeedPerReadable: (flaskVars(flaskName).surArea * inputInfo.density).toLocaleString('en-US'),
          cellYieldPerReadable: (flaskVars(flaskName).surArea * inputInfo.confluentDensity).toLocaleString('en-US'),
          mediaPer: flaskVars(flaskName).mediaVol,
          tryplePer: flaskVars(flaskName).trypleVol,
        };
      };
    };
  };
  return( returnVar);
};


var flaskVars = function calculateFlaskVars(flaskName) {

  if (flaskName == 'T25'){
    surArea = flaskT25.surArea;
    mediaVolume = flaskT25.media;
    trypleVolume = flaskT25.tryple;
  }

  if (flaskName == 'T75'){
    surArea = flaskT75.surArea;
    mediaVolume = flaskT75.media;
    trypleVolume = flaskT75.tryple;
  }

  if (flaskName == 'T225'){
    surArea = flaskT225.surArea;
    mediaVolume = flaskT225.media;
    trypleVolume = flaskT225.tryple;
  }

  if (flaskName == 'CS5'){
    surArea = flaskCS5.surArea;
    mediaVolume = flaskCS5.media;
    trypleVolume = flaskCS5.tryple;
  }

  if (flaskName == 'CS10'){
    surArea = flaskCS10.surArea;
    mediaVolume = flaskCS10.media;
    trypleVolume = flaskCS10.tryple;
  }


  return {
    flaskName: flaskName,
    surArea: surArea,
    mediaVol: mediaVolume,
    trypleVol: trypleVolume,
    };

};


//var confluentCellDensity = 35000;

var T25 = {
  surArea: 25,
  media: 5,
  tryple: 1,
};

var T75 = {
  surArea: 75,
  media: 15,
  tryple: 3,
};

var T225 = {
  surArea: 225,
  media: 45,
  tryple: 10,
};

var CS1 = {
  surArea: 1272*1,
  media: 750/5,
  tryple: 100/5,
};

var CS2 = {
  surArea: 1272*2,
  media: 750/5*2,
  tryple: 100/5*2,
};

var CS5 = {
  surArea: 1272*5,
  media: 750,
  tryple: 100,
};

var CS10 = {
  surArea: 1272*10,
  media: 1500,
  tryple: 200,
};

var flaskNames = ['CS10', 'CS5','T225','T75','T25' ];
