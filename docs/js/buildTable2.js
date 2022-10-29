

document.getElementById("calculate-button").addEventListener("click", function(){

  var cells = document.getElementById('tentacles1').value;
  cells = cells*1E6;
  var density = document.getElementById('tentacles2').value;
  var passages = document.getElementById('tentacles3').value;
  var confluentCellDensity = document.getElementById('tentacles4').value;

  var inputInfo = {
    cells: cells,
    density: density*1,
    passages: passages*1,
    confluentCellDensity: confluentCellDensity*1,
    passage: passages*1,
    cellsEstimate: cells,
  };

  var tableFlasks = buildTableData(inputInfo);

  myFunction(tableFlasks);



});

// Function to build table data
function buildTableData(inputInfo){

  var allMediaTotal = mediaTotal(inputInfo)

  var tableFlasks = [
    {
      'Col1': 'Target Cell Yield',
      'Col3': (inputInfo.cells).toLocaleString('en-US'),
      'Col4': 'cells'
    } , {
      'Col1': 'Passages from Initial Plating to Final Cell Yield',
      'Col3': inputInfo.passages,
      'Col4': 'passages'
    } ,  {
      'Col1': 'Target Cell Seeding Density',
      'Col3':  inputInfo.density,
      'Col4': 'cells/cm2'
    } , {
      'Col1': 'Confluent Cell Density',
      'Col3':  inputInfo.confluentCellDensity.toLocaleString('en-US'),
      'Col4': 'cells/cm2'
    } , {
      'Col1': ' ',
      'Col3': ' ',
      'Col4': ' '
    } , {
      'Col1': 'Cell Yield',
      'Col3': allMediaTotal.cellYieldFinalReadable,
      'Col4': 'cells'
    } , {
      'Col1': 'Cell Seeded',
      'Col3': allMediaTotal.cellSeededInitialReadable,
      'Col4': 'cells'
    } , {
      'Col1': 'Media Volume',
      'Col3': allMediaTotal.mediaVolTotal,
      'Col4': 'mL'
    } , {
      'Col1': 'TrypLe Volume',
      'Col3': allMediaTotal.trypleVolTotal,
      'Col4': 'mL',
    } , {
      'Col1': 'Media Bottles',
      'Col3': allMediaTotal.mediaBottles,
      'Col4': 'mL'
    } , {
      'Col1': 'Predicted Overfill',
      'Col3': allMediaTotal.overfill,
      'Col4': '%'
    } , {
      'Col1': '',
      'Col2': '',
      'Col3': '',
      'Col4': ''
    } ,
  ];

  var passage_table = [];

  for (let j = inputInfo.passages; j>0; j--) {

    console.log('j = ')
    console.log(j)

    inputInfo.passage = j;
    console.log('inputInfo.passage = ')
    console.log(inputInfo.passage)

    inputInfo.last = Preturn;
    if (inputInfo.passage == 1){
      inputInfo.P2 = Preturn;
    };

    console.log('inputInfo = ')
    console.log(inputInfo)

    if (inputInfo.passage == inputInfo.passages) {
      inputInfo.cellsEstimate = inputInfo.cells;
    }
    else {
      inputInfo.cellsEstimate = Preturn.cellsSeedTotal;
    };

    var Preturn = Pchars(inputInfo);
    console.log('Preturn = ')
    console.log(Preturn)

    if (inputInfo.passage == 1){
      inputInfo.P1 = Preturn;
    };
    if (inputInfo.passage == 2){
      inputInfo.P2 = Preturn;
    };
    if (inputInfo.passage == 3){
      inputInfo.P3 = Preturn;
    };
    if (inputInfo.passage == 3){
      inputInfo.P4 = Preturn;
    };
    if (inputInfo.passage == 3){
      inputInfo.P5 = Preturn;
    };

    var add = [
      {
        'Col1': 'P' + inputInfo.passage + ' Flask Type',
        'Col3': Preturn.flaskType,
        'Col4': 'flasks'
      } , {
        'Col1': 'P' + inputInfo.passage + ' Flask Count',
        'Col3': Preturn.flaskCount,
        'Col4': 'flasks'
      } , {
        'Col1': 'P' + inputInfo.passage + ' Cell Yield Total ',
        'Col3': Preturn.cellsYieldTotalReadable,
        'Col4': 'cells'
      } , {
        'Col1': 'P' + inputInfo.passage + ' Cell Yield Per Flask ',
        'Col3': Preturn.cellsYieldPerReadable,
        'Col4': 'cells'
      } , {
        'Col1': 'P' + inputInfo.passage + ' Cell Seed Total ',
        'Col3': Preturn.cellsSeedTotalReadable,
        'Col4': 'cells'
      } , {
        'Col1': 'P' + inputInfo.passage + ' Cell Seed Per Flask ',
        'Col3': Preturn.cellsSeedPerReadable,
        'Col4': 'cells'
      } , {
        'Col1': 'P' + inputInfo.passage + ' Media Volume - Bottles ',
        'Col3': Preturn.mediaBottles,
        'Col4': 'bottles media'
      } , {
        'Col1': 'P' + inputInfo.passage + ' Media Volume - Total ',
        'Col3': Preturn.mediaVol,
        'Col4': 'mL'
      } , {
        'Col1': 'P' + inputInfo.passage + ' TrypLe Volume - Total ',
        'Col3': Preturn.trypleVol,
        'Col4': 'mL'
      } , {
        'Col1': 'P' + inputInfo.passage + ' Media Volume - Each Flask ',
        'Col3': Preturn.mediaVolPer,
        'Col4': 'mL'
      } , {
        'Col1': 'P' + inputInfo.passage + ' TrypLe Volume - Each Flask ',
        'Col3': Preturn.trypleVolPer,
        'Col4': 'mL'
      } , {
        'Col1': ' ',
        'Col3': ' ',
        'Col4': ' '
      } ,
      ];

      for (let i = 0; i < add.length; i++) {
        passage_table.push(add[i]);
      }
  }


  for (let i = 0; i < passage_table.length; i++) {
    tableFlasks.push(passage_table[i]);
  }

  var end = [
      {'Col1': '', 'Col2': '', 'Col3': '', 'Col4': ''} ,
      {'Col1': '', 'Col2': '', 'Col3': '', 'Col4': ''} ,
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
        paginationSize:50,         //allow 7 rows per page of data
        paginationCounter:"rows", //display count of paginated rows in footer
        movableColumns:true,      //allow column order to be changed
        initialSort:[             //set the initial sort order of the data
            {column:"name", dir:"asc"},
        ],
        columns:[                 //define the table columns
            {title:"Name", field:"Col1", editor:"input"},
            //{title:"URL", field:"Col2", width:150, formatter:"link", formatterParams:{target:"_blank",}},
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
