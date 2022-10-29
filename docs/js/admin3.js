//var confluentCellDensity = 35000;

var flaskT25 = {
  surArea: 25,
  media: 5,
  tryple: 1,
};

var flaskT75 = {
  surArea: 75,
  media: 15,
  tryple: 3,
};

var flaskT225 = {
  surArea: 225,
  media: 45,
  tryple: 10,
};

var flaskCS5 = {
  surArea: 1272*5,
  media: 750,
  tryple: 100,
};

var flaskCS10 = {
  surArea: 1272*10,
  media: 1500,
  tryple: 200,
};

var flaskNames = ['CS10', 'CS5','T225','T75','T25' ];


var Pchars = function functionPnewchars(inputInfo) {

  var cells = inputInfo.cells;
  var density = inputInfo.density;
  var passages = inputInfo.passages;
  var confluentCellDensity = inputInfo.confluentCellDensity;
  var passage = inputInfo.passage;
  var cellsEstimate = inputInfo.cellsEstimate;

  if (inputInfo.passage = inputInfo.passages) {
    var cellsEstimate = inputInfo.cells;
  }
  else{
    var cellsEstimate = inputInfo.last.cellSeedTotal;
    console.log('cellEstimate not equal to cells = ')
    console.log(cellsEstimate)
  };

  console.log('cellsEstimate = ')
  console.log(cellsEstimate)
  console.log('passage = ')
  console.log(passage)

  var flaskCountLowest = 10**100;

  for (let i = 0; i<=flaskNames.length; i++) {

    var surfaceArea = flaskVars(flaskNames[i]).surArea;

    var flaskCount =  cellsEstimate / (surfaceArea * confluentCellDensity);

    if (flaskCount > 1){

      flaskCount = Math.ceil(flaskCount);

      if (flaskCount <= flaskCountLowest){

        flaskCountLowest = flaskCount;

        var mediaVolTemp = flaskVars(flaskNames[i]).mediaVol + 2*flaskVars(flaskNames[i]).trypleVol;

        var returnVar = {
          cells: cells,
          cellsReadable: cells.toLocaleString('en-US'),
          cellsEstimate: cellsEstimate,
          flaskCount: flaskCount,
          flaskType: flaskNames[i],
          mediaBottles: mediaVolTemp * flaskCount/500,
          mediaVol: mediaVolTemp * flaskCount,
          trypleVol: flaskVars(flaskNames[i]).trypleVol * flaskCount,
          mediaVolPer: flaskVars(flaskNames[i]).mediaVol,
          trypleVolPer: flaskVars(flaskNames[i]).trypleVol,
          cellsSeedPerReadable: (flaskVars(flaskNames[i]).surArea * density).toLocaleString('en-US'),
          cellsSeedTotal: (flaskVars(flaskNames[i]).surArea * density*flaskCount),
          cellsSeedTotalReadable: (flaskVars(flaskNames[i]).surArea * density*flaskCount).toLocaleString('en-US'),
          cellsYieldPer: flaskVars(flaskNames[i]).surArea * confluentCellDensity,
          cellsYieldTotal: flaskVars(flaskNames[i]).surArea * confluentCellDensity * flaskCount,
          cellsYieldPerReadable: (flaskVars(flaskNames[i]).surArea * confluentCellDensity).toLocaleString('en-US'),
          cellsYieldTotalReadable: (flaskVars(flaskNames[i]).surArea * confluentCellDensity * flaskCount).toLocaleString('en-US'),
        };
      };
    };
  };
  return  returnVar;
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


var mediaTotal = function functionmediaTotal(inputInfo){

  var mediaVolTotal = 0;
  var trypleVolTotal = 0;
  var RoosterGem = 0;
  var RoosterEV = 0;

  for (let j = inputInfo.passages; j>0; j--) {

    inputInfo.passage = j;
    var Pfound = Pchars(inputInfo)

    mediaVolTotal = mediaVolTotal + Pfound.mediaVol;
    trypleVolTotal = trypleVolTotal + Pfound.trypleVol;
    mediaBottles =  Math.ceil(mediaVolTotal/500);

    if (inputInfo.passage = 1){
      RoosterGem = Pfound.mediaVol;
    };
    if (inputInfo.passages == 1){
      var cellSeededInitial = 1*Pfound.cellsSeedTotal;
    };
    if (inputInfo.passages == j){
      RoosterEV = Pfound.mediaVol;
    };
    if (inputInfo.passages == j){
      var cellYieldFinal = 1*Pfound.cellsYieldTotal;
    };
    if (inputInfo.passages == j){
      var overfill = Math.round(Pfound.cellsYieldTotal/Pfound.cells * 100 -100 , 2);
    };

  };

  return {
    mediaVolTotal: mediaVolTotal,
    trypleVolTotal: trypleVolTotal,
    mediaBottles: mediaBottles,
    RoosterGem: RoosterGem,
    RoosterEV: RoosterEV,
    RoosterGemBottles: RoosterGem/200,
    RoosterEVBottles: RoosterGem/500,
    cellSeededInitial: cellSeededInitial,
    cellYieldFinal: cellYieldFinal,
    cellSeededInitialReadable: (1*cellSeededInitial).toLocaleString('en-US'),
    cellYieldFinalReadable: (1*cellYieldFinal).toLocaleString('en-US'),
    overfill: overfill
  };
};
