var ResearchMedia = 'https://www.roosterbio.com/products/roosternourish-msc-kt-001/';

document.getElementById("calculate-button").addEventListener("click", function(){

  var cells = document.getElementById('tentacles1').value;
  var density = document.getElementById('tentacles2').value;
  var passages = document.getElementById('tentacles3').value;

  var Initialcells = cellsInitial(cells, passages)
  console.log('Initialcells =')
  console.log(Initialcells.initial)
  console.log(Initialcells.initialReadable)

  var flaskware = eligibleFlaskware(cells, passages)

  console.log('flaskware = ')
  console.log(flaskware) 


  //var cells  = output1.innerHTML;
  //var density  = output2.innerHTML;
  //var passages  = output3.innerHTML;
  console.log(cells);
  console.log(density);
  //var cells = quantity.innerHTML;
  //console.log(cells)

  var tableFlasks = buildTableData(cells, density, passages);

  myFunction(tableFlasks);



});


function calculateCellNumbers(cells, density, passages){

  var yield = cells;
  yield = yield*1000000;
  var cellPassageCounts = {yield: yield.toLocaleString('en-US')}

  if (passages == 1){
    var P1cellPlated = cells/10;
    var P1cellYield = cells*1;

    P1cellPlated = P1cellPlated.toLocaleString('en-US');
    P1cellYield = P1cellYield.toLocaleString('en-US');
    var cellPassageCounts = {P1cellPlated: P1cellPlated, P1cellYield: P1cellYield};
  };

  if (passages == 2){
    var P1cellPlated = 1E6*cells/100;
    var P1cellYield = 1E6*cells/10;
    var P2cellPlated = 1E6*cells/10;
    var P2cellYield = 1E6*cells*1;

    yield = yield.toLocaleString('en-US');
    P1cellPlated = P1cellPlated.toLocaleString('en-US');
    P1cellYield = P1cellYield.toLocaleString('en-US');
    P2cellPlated = P2cellPlated.toLocaleString('en-US');
    P2cellYield = P2cellYield.toLocaleString('en-US');

    cellPassageCounts['P1cellPlated'] = P1cellPlated;
    cellPassageCounts['P1cellYield'] = P1cellYield;
    cellPassageCounts['P2cellPlated'] = P2cellPlated;
    cellPassageCounts['P2cellYield'] = P2cellYield;

  };

  if (passages == 3){
    var P1cellPlated = cells/1000;
    var P1cellYield = cells/100;
    var P2cellPlated = cells/100;
    var P2cellYield = cells/10;
    var P3cellPlated = cells/10;
    var P3cellYield = cells/1;

    cellPassageCounts['P1cellPlated'] = 1E6*P1cellPlated.toLocaleString('en-US');
    cellPassageCounts['P1cellYield'] = 1E6*P1cellYield.toLocaleString('en-US');
    cellPassageCounts['P2cellPlated'] = 1E6*P2cellPlated.toLocaleString('en-US');
    cellPassageCounts['P2cellYield'] = 1E6*P2cellYield.toLocaleString('en-US');
    cellPassageCounts['P3cellPlated'] = 1E6*P3cellPlated.toLocaleString('en-US');
    cellPassageCounts['P3cellYield'] = 1E6*P3cellYield.toLocaleString('en-US');

  };

  if (passages == 4){
    var P1cellPlated = 1E6*cells/10000;
    var P1cellYield = 1E6*cells/1000;
    var P2cellPlated = 1E6*cells/1000;
    var P2cellYield = 1E6*cells/100;
    var P3cellPlated = 1E6*cells/100;
    var P3cellYield = 1E6*cells/10;
    var P4cellPlated = 1E6*cells/10;
    var P4cellYield = 1E6*cells/1;

    cellPassageCounts['P1cellPlated'] = P1cellPlated.toLocaleString('en-US');
    cellPassageCounts['P1cellYield'] = P1cellYield.toLocaleString('en-US');
    cellPassageCounts['P2cellPlated'] = P2cellPlated.toLocaleString('en-US');
    cellPassageCounts['P2cellYield'] = P2cellYield.toLocaleString('en-US');
    cellPassageCounts['P3cellPlated'] = P3cellPlated.toLocaleString('en-US');
    cellPassageCounts['P3cellYield'] = P3cellYield.toLocaleString('en-US');
    cellPassageCounts['P4cellPlated'] = P4cellPlated.toLocaleString('en-US');
    cellPassageCounts['P4cellYield'] = P4cellYield.toLocaleString('en-US');

  };

return(cellPassageCounts)

}


function calculateMedia(cells, seedingDensity, passages, flaskName){

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

  surArea = Number(surArea)
  mediaVolume = Number(mediaVolume)
  trypleVolume = Number(trypleVolume)

  cells = cells*1E6
  var cellsInitial = cells/10;

  var count = cellsInitial/seedingDensity/surArea;
  var count = Math.ceil(Number(count));

  var media = count*(mediaVolume + trypleVolume*2);

  var bottles = Math.ceil(Number(media/500));

  var cellPerFlask = Math.ceil(Number(seedingDensity*surArea));

  count = count.toLocaleString('en-US');

  var density = seedingDensity*1

  return {
    cells: cells.toLocaleString('en-US'),
    density: density.toLocaleString('en-US'),
    count: count,
    media: media.toLocaleString('en-US'),
    bottles:  bottles,
    cellPerFlask: cellPerFlask.toLocaleString('en-US')
    };
}


// Function to build table data
function buildTableData(cells, density, passages){

  var cellPassageCounts = calculateCellNumbers(cells, density, passages);

  var T25 = calculateMedia(cells, density, passages, 'T25')
  var T75 = calculateMedia(cells, density, passages, 'T75')
  var T225 = calculateMedia(cells, density, passages, 'T225')
  var CS5 = calculateMedia(cells, density, passages, 'CS5')
  var CS10 = calculateMedia(cells, density, passages, 'CS10')


  if (cells > 90){
    let name = CS10.bottles + ' ' + 'bottles of media in ' + CS10.count + 'x CellStack-10 flasks';
    document.getElementById("name").innerHTML = name;
  }
  else{
    let name = ' ';
    document.getElementById("name").innerHTML = name;
  }

  let name2 = ' '
  if (cells > 40){
  let name2 = CS5.bottles + ' ' + 'bottles of media in ' + CS5.count + 'x CellStack-5 flasks';
  document.getElementById("name2").innerHTML = name2;
  }
  else{
    let name2 = ' ';
    document.getElementById("name2").innerHTML = name2;
  }


  if (cells < 201){
  let name3 = T225.bottles + ' ' + 'bottles of media in ' + T225.count + 'x T225 flasks';
  document.getElementById("name3").innerHTML = name3;
  }
  else{
    let name3 = ' ';
    document.getElementById("name3").innerHTML = name3;
  }







  var tableFlasks =
  [
    {'Col1': 'Target Cell Yield', 'Col3': cellPassageCounts.P4cellYield , 'Col4': 'cells'} ,
    {'Col1': 'Target Cell Seeding Density', 'Col3': T25.density, 'Col4': 'cells/cm2'} ,
    {'Col1': 'Passages from Initial Plating to Final Cell Yield', 'Col3': passages, 'Col4': 'passages'} ,
    {'Col1': '', 'Col2': '', 'Col3': '', 'Col4': ''} ,
  ];

  var passage_table = [];

  if (passages >= 1){
    var add = [
      {'Col1': 'P1 Plating Cell Count', 'Col3': cellPassageCounts.P1cellPlated, 'Col4': 'cells'} ,
      {'Col1': 'P1 Expanded Cell Count', 'Col3': cellPassageCounts.P1cellYield, 'Col4': 'cells'} ,
      ];

      for (let i = 0; i < add.length; i++) {
        passage_table.push(add[i]);
      }
  }

  if (passages >= 2){
    var add = [
      {'Col1': 'P2 Plating Cell Count', 'Col3': cellPassageCounts.P2cellPlated, 'Col4': 'cells'} ,
      {'Col1': 'P2 Expanded Cell Count', 'Col3': cellPassageCounts.P2cellYield, 'Col4': 'cells'} ,
      ];

      for (let i = 0; i < add.length; i++) {
        passage_table.push(add[i]);
      }
  }

  if (passages >= 3){
    var add = [
      {'Col1': 'P3 Plating Cell Count', 'Col3': cellPassageCounts.P3cellPlated, 'Col4': 'cells'} ,
      {'Col1': 'P3 Expanded Cell Count', 'Col3': cellPassageCounts.P3cellYield, 'Col4': 'cells'} ,
      ];

      for (let i = 0; i < add.length; i++) {
        passage_table.push(add[i]);
      }
  }

  if (passages >= 4){
    var add = [
      {'Col1': 'P4 Plating Cell Count', 'Col3': T25.cellsPlatedP1, 'Col4': 'cells'} ,
      {'Col1': 'P4 Expanded Cell Count', 'Col3': T25.cellsYieldP1, 'Col4': 'cells'} ,
      ];

      for (let i = 0; i < add.length; i++) {
        passage_table.push(add[i]);
      }
  }

  if (passages >= 5){
    var add = [
      {'Col1': 'P5 Plating Cell Count', 'Col3': T25.cellsPlatedP1, 'Col4': 'cells'} ,
      {'Col1': 'P5 Expanded Cell Count', 'Col3': T25.cellsYieldP1, 'Col4': 'cells'} ,
      ];

      for (let i = 0; i < add.length; i++) {
        passage_table.push(add[i]);
      }
  }


  for (let i = 0; i < passage_table.length; i++) {
    tableFlasks.push(passage_table[i]);
  }

  var end =
    [

      {'Col1': '', 'Col2': '', 'Col3': '', 'Col4': ''} ,
      {'Col1': 'Cell Stack-10 (CS10)', 'Col2': '', 'Col3': '', 'Col4': ''} ,
      {'Col1': 'Flasks - Total', 'Col2': '', 'Col3': CS10.count, 'Col4': 'flasks'} ,
      {'Col1': 'Cells Seeded per Flask', 'Col2': '', 'Col3': CS10.cellPerFlask, 'Col4': 'cells'} ,
      {'Col1': 'Media Volume per Flask', 'Col2': '', 'Col3': flaskCS10.media, 'Col4': 'mL'} ,
      {'Col1': 'Media Volume - Total', 'Col2': '', 'Col3': CS10.media, 'Col4': 'mL'} ,
      {'Col1': 'Media Bottles - Total', 'Col2': ResearchMedia, 'Col3': CS10.bottles, 'Col4': 'bottles'},

      {'Col1': '', 'Col2': '', 'Col3': '', 'Col4': ''} ,
      {'Col1': 'Flasks - Total', 'Col2': '', 'Col3': '', 'Col4': ''} ,
      {'Col1': 'Cell Stack-5 (CS5) - Total', 'Col2': '', 'Col3': CS5.count, 'Col4': 'flasks'} ,
      {'Col1': 'Cells Seeded per Flask', 'Col2': '', 'Col3': CS5.cellPerFlask, 'Col4': 'cells'} ,
      {'Col1': 'Media Volume per Flask', 'Col2': '', 'Col3': flaskCS5.media, 'Col4': 'mL'} ,
      {'Col1': 'Media Volume - Total', 'Col2': '', 'Col3': CS5.media, 'Col4': 'mL'} ,
      {'Col1': 'Media Bottles - Total', 'Col2': ResearchMedia, 'Col3': CS5.bottles, 'Col4': 'bottles'} ,

      {'Col1': '', 'Col2': '', 'Col3': '', 'Col4': ''} ,
      {'Col1': 'T225', 'Col2': '', 'Col3': '', 'Col4': ''} ,
      {'Col1': 'Flasks - Total', 'Col2': '', 'Col3': T225.count, 'Col4': 'flasks'} ,
      {'Col1': 'Cells Seeded per Flask', 'Col2': '', 'Col3': T225.cellPerFlask, 'Col4': 'cells'} ,
      {'Col1': 'Media Volume per Flask', 'Col2': '', 'Col3': flaskT225.media, 'Col4': 'mL'} ,
      {'Col1': 'Media Volume - Total', 'Col2': '', 'Col3': T225.media, 'Col4': 'mL'} ,
      {'Col1': 'Media Bottles - Total', 'Col2': ResearchMedia, 'Col3': T225.bottles, 'Col4': 'bottles'},

      {'Col1': '', 'Col2': '', 'Col3': '', 'Col4': ''} ,
      {'Col1': 'T75', 'Col2': '', 'Col3': '', 'Col4': ''} ,
      {'Col1': 'Flasks - Total', 'Col2': '', 'Col3': T75.count, 'Col4': 'flasks'} ,
      {'Col1': 'Cells Seeded per Flask', 'Col2': '', 'Col3': T75.cellPerFlask, 'Col4': 'cells'} ,
      {'Col1': 'Media Volume per Flask', 'Col2': '', 'Col3': flaskT75.media, 'Col4': 'mL'} ,
      {'Col1': 'Media Volume - Total', 'Col2': '', 'Col3': T75.media, 'Col4': 'mL'} ,
      {'Col1': 'Media Bottles - Total', 'Col2': ResearchMedia, 'Col3': T75.bottles, 'Col4': 'bottles'} ,

      {'Col1': '', 'Col2': '', 'Col3': '', 'Col4': ''} ,
      {'Col1': 'T25', 'Col2': '', 'Col3': '', 'Col4': ''} ,
      {'Col1': 'Flasks - Total', 'Col2': '', 'Col3': T25.count, 'Col4': 'flasks'} ,
      {'Col1': 'Cells Seeded per Flask', 'Col2': '', 'Col3': T25.cellPerFlask, 'Col4': 'cells'} ,
      {'Col1': 'Media Volume per Flask', 'Col2': '', 'Col3': flaskT25.media, 'Col4': 'mL'} ,
      {'Col1': 'Media Volume - Total', 'Col2': '', 'Col3': T25.media, 'Col4': 'mL'} ,
      {'Col1': 'Media Bottles - Total', 'Col2': ResearchMedia, 'Col3': T25.bottles, 'Col4': 'bottles'} ,


      ];


  for (let i = 0; i < end.length; i++) {
      tableFlasks.push(end[i]);
    }

  return(tableFlasks)
}


// Function to build table
function myFunction(tableFlasks) {


    var table = new Tabulator("#tabularRooster", {
        data:tableFlasks,           //load row data from array
        layout:"fitColumns",      //fit columns to width of table
        responsiveLayout:"hide",  //hide columns that dont fit on the table
        tooltips:true,            //show tool tips on cells
        addRowPos:"top",          //when adding a new row, add it to the top of the table
        history:true,             //allow undo and redo actions on the table
        pagination:"local",       //paginate the data
        paginationSize:8,         //allow 7 rows per page of data
        paginationCounter:"rows", //display count of paginated rows in footer
        movableColumns:true,      //allow column order to be changed
        initialSort:[             //set the initial sort order of the data
            {column:"name", dir:"asc"},
        ],
        columns:[                 //define the table columns
            {title:"Name", field:"Col1", editor:"input"},
            {title:"URL", field:"Col2", width:150, formatter:"link", formatterParams:{target:"_blank",}},
            {title:"Quantity", field:"Col3", width:150, editor:"input"},
            {title:"Unit", field:"Col4", width:150, editor:"input"},
          //  {title:"Task Progress", field:"progress", hozAlign:"left", formatter:"progress", editor:true},
          //  {title:"Gender", field:"gender", width:95, editor:"select", editorParams:{values:["male", "female"]}},
          //  {title:"Rating", field:"rating", formatter:"star", hozAlign:"center", width:100, editor:true},
            //{title:"Color", field:"col", width:130, editor:"input"},
            //{title:"Date Of Birth", field:"dob", width:130, sorter:"date", hozAlign:"center"},
            //{title:"Driver", field:"car", width:90,  hozAlign:"center", formatter:"tickCross", sorter:"boolean", editor:true},
        ],
    });


    //trigger download of data.xlsx file
    document.getElementById("download-csv").addEventListener("click", function(){
        table.download("csv", "RoosterBio.csv");
    });

    document.getElementById("download-xlsx").addEventListener("click", function(){
        table.download("xlsx", "RoosterBio.xlsx", {sheetName:"My Data"});
    });

}
