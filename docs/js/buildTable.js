document.getElementById("calculate-button").addEventListener("click", function(){

  var cells = document.getElementById('tentacles1').value;
  cells = cells*1E6;
  var density = document.getElementById('tentacles2').value;
  var passages = document.getElementById('tentacles3').value;
  var confluentDensity = document.getElementById('tentacles4').value;

  var inputInfo = {
    cells: cells,
    density: density*1,
    passages: passages*1,
    confluentDensity: confluentDensity*1,
    passage: passages*1,
    cellsEstimate: cells,
    deltaPDL: 0,
    last: {cellSeed: cells, deltaPDL: 0},
  };

  var passageCalcs = calculatePassages(inputInfo);

  console.log('passageCalcs = ')
  console.log(passageCalcs)

  var tableFlasks = buildTableData(inputInfo, passageCalcs);

  let name = passageCalcs.mediaDescLong ;
  document.getElementById("name").innerHTML = name;

  let name2 = passageCalcs.flaskDesc;
  document.getElementById("name2").innerHTML = name2;

  let name3 = Math.ceil(passageCalcs.RoosterGem/200) + ' RoosterGEM Bottles (200mL/bottle)';
  document.getElementById("name3").innerHTML = name3;

  let name4 = (passageCalcs.EVCollect).toLocaleString('en-US') + ' mL RoosterCollect-EV';
  document.getElementById("name4").innerHTML = name4;

  let name5 = passageCalcs.cellSeedTotalReadable + ' cells';
  document.getElementById("name5").innerHTML = name5;

  myFunction(tableFlasks);

});


// Function to build table data
function buildTableData(inputInfo, passageCalcs){

  var tableFlasks = [
    {
      'Col1': 'Target Cell Yield',
      'Col3': (passageCalcs.cells).toLocaleString('en-US'),
      'Col4': 'cells'
    } , {
      'Col1': 'Passages from Initial Plating to Final Cell Yield',
      'Col3': passageCalcs.passages,
      'Col4': 'passages'
    } ,  {
      'Col1': 'Target Cell Seeding Density',
      'Col3':  passageCalcs.density.toLocaleString('en-US'),
      'Col4': 'cells/cm2'
    } , {
      'Col1': 'Confluent Cell Density',
      'Col3':  passageCalcs.confluentDensity.toLocaleString('en-US'),
      'Col4': 'cells/cm2'
    } , {
      'Col1': ' ',
      'Col3': ' ',
      'Col4': ' '
    } , {
      'Col1': 'Cell Yield',
      'Col3': passageCalcs.cellYieldTotalReadable,
      'Col4': 'cells'
    } , {
      'Col1': 'Cell Seeded',
      'Col3': passageCalcs.cellSeedTotalReadable,
      'Col4': 'cells'
    } , {
      'Col1': 'Media Volume (including 1xTrypLe volume to quench)',
      'Col3': passageCalcs.mediaTotal.toLocaleString('en-US'),
      'Col4': 'mL'
    } , {
      'Col1': 'TrypLe Volume',
      'Col3': passageCalcs.trypleTotal.toLocaleString('en-US'),
      'Col4': 'mL',
    } , {
      'Col1': 'Media Bottles (500mL each)',
      'Col3': passageCalcs.mediaBottles,
      'Col4': 'bottles'
    } , {
      'Col1': 'Predicted Overfill',
      'Col3': passageCalcs.overfill,
      'Col4': '%'
    } , {
      'Col1': 'Flaskware Description (with XF media, use Corning CellBind or a vitronectin coating)',
      'Col3': passageCalcs.flaskDesc,
      'Col4': ' '
    } , {
      'Col1': 'Passage Increase',
      'Col3': '+ ' + inputInfo.passages,
      'Col4': 'Passages'
    } , {
      'Col1': 'Population Doubling Level (PDL) Increase',
      'Col3': '+ ' + inputInfo.passages*inputInfo.deltaPDL,
      'Col4': 'PDL'
    } , {
      'Col1': '',
      'Col2': '',
      'Col3': '',
      'Col4': ''
    } ,
  ];

  var passage_table = [];

  console.log('inputInfo.passages = ')
  console.log(inputInfo.passages)

  for (let m = inputInfo.passages; m>0; m--) {

    if (m == 2){
      var passageInfo = passageCalcs.P2;
    }
    else if (m == 1) {
      var passageInfo = passageCalcs.P1;
    }
    else if (m == 3) {
      var passageInfo = passageCalcs.P3;
    }
    else if (m == 4){
      var passageInfo = passageCalcs.P4;
    }
    else {
      var passageInfo = passageCalcs.P1;
    };

    console.log('m = ')
    console.log(m)
    console.log('passageInfo = ')
    console.log(passageInfo)
    console.log('passageInfo.flaskType = ')
    console.log(passageInfo.flaskType)

    var add = [
        {
          'Col1': 'P' + m + ' Flask Type (with XF media, use Corning CellBind or a vitronectin coating)',
          'Col3': passageInfo.flaskType,
          'Col4': 'flasks'
        } , {
          'Col1': 'P' + m + ' Flask Count',
          'Col3': passageInfo.flaskCount,
          'Col4': 'flasks'
        }, {
          'Col1': 'P' + m + ' Cells Seeded Total',
          'Col3': passageInfo.cellSeedReadable,
          'Col4': 'cells'
        }, {
          'Col1': 'P' + m + ' Cells Yield Total',
          'Col3': passageInfo.cellYieldReadable,
          'Col4': 'cells'
        }, {
          'Col1': 'P' + m + ' Media Total (including 1xTrypLe volume to quench)',
          'Col3': passageInfo.mediaTotal.toLocaleString('en-US'),
          'Col4': 'mL'
        }, {
          'Col1': 'P' + m + ' TrypLe Total',
          'Col3': passageInfo.trypleTotal.toLocaleString('en-US'),
          'Col4': 'mL'
        }, {
          'Col1': 'P' + m + ' Cell Seed Per Flask',
          'Col3': passageInfo.cellSeedPerReadable,
          'Col4': 'cell'
        }, {
          'Col1': 'P' + m + ' Cell Yield Per Flask',
          'Col3': passageInfo.cellYieldPerReadable,
          'Col4': 'cell'
        }, {
          'Col1': 'P' + m + ' Media Per Flask (no media exchange needed with RoosterNourish)',
          'Col3': passageInfo.mediaPer,
          'Col4': 'cell'
        }, {
          'Col1': 'P' + m + ' TrypLe Per Flask',
          'Col3': passageInfo.tryplePer,
          'Col4': 'cell'
        }, {
          'Col1': 'P' + m + ' Surface Area Per Flask',
          'Col3': passageInfo.surArea,
          'Col4': 'cm2'
        }, {
          'Col1': 'P' + m + ' Population Doubling Level (PDL) Increase',
          'Col3': '+ ' + passageInfo.deltaPDL,
          'Col4': 'PDL'
        }, {
          'Col1': ' ',
          'Col3': ' ',
          'Col4': ' ',
        },
        ];
    console.log('add = ')
    console.log(add);

    for (let i = 0; i < add.length; i++) {
        passage_table.push(add[i]);
    };

    console.log('passage_table = ')
    console.log(passage_table)
  };


  for (let i = 0; i < passage_table.length; i++) {
    tableFlasks.push(passage_table[i]);
  };

  var end = [
      {'Col1': 'Get the most out of your media.', 'Col2': '', 'Col3': '', 'Col4': ''} ,
      {'Col1': '1. Avoid temperature cycling the media, including components. This will compromise quality.',  'Col4': ''} ,
      {'Col1': '2. Avoid water baths to warm media. Instead equilibrate the media, including components, to room temperature out of direct light. The formula is sensitive to photo- and thermal-degradation.',  'Col4': ''},
      {'Col1': '3. Skip media changes, even half changes, between passages.', 'Col4': ''},
      {'Col1': '4. For Xeno-Free media culture, use Corning CellBind flaskware or a vitronectin coating, otherwise cell attachment will be inconsistent and poor.', 'Col4': ''},
      {'Col1': '5. Passage the cells at 80-90% confluent. Overly confluent cells may enter a lag phase of growth, which will reduce the total cell yield or delay cell growth. Also, overly confluent cells may produce extracellular matrix, which makes the cells aggregate in suspension. Passaging a little too early is better than a little too late.',  'Col4': ''},
      {'Col1': ' ', 'Col2': '', 'Col3': '', 'Col4': ''} ,
      {'Col1': 'Contact us for more information:', 'Col3': 'https://www.roosterbio.com/contact/', 'Col4': ''} ,
      {'Col1': 'CS10 - CellStack-10', 'Col3': 'https://ecatalog.corning.com/life-sciences/b2c/US/en/Browse-Products-by-Application/Cell-Therapy-and-Vaccines/CellSTACK%C2%AE/Corning%C2%AE-CellSTACK%C2%AE-Culture-Chambers/p/3271', 'Col4': ''} ,
      {'Col1': 'CS5 - CellStack-5', 'Col3': 'https://ecatalog.corning.com/life-sciences/b2c/US/en/Browse-Products-by-Application/Cell-Therapy-and-Vaccines/CellSTACK%C2%AE/Corning%C2%AE-CellSTACK%C2%AE-Culture-Chambers/p/3313', 'Col4': ''} ,
      {'Col1': 'T225 - Flask', 'Col2': '', 'Col4': ''} ,
      {'Col1': 'T75 - Flask', 'Col2': '', 'Col3': '', 'Col4': ''} ,
      {'Col1': 'T25 - Flask', 'Col2': '', 'Col3': '', 'Col4': ''} ,
      {'Col1': 'For XF Media: Corning CellBind Flaskware', 'Col3': 'https://ecatalog.corning.com/life-sciences/b2c/US/en/Browse-Products-by-Application/Cell-Therapy-and-Vaccines/CellSTACK%C2%AE/Corning%C2%AE-CellSTACK%C2%AE-Culture-Chambers/p/corningCellSTACKCultureChambers', 'Col4': ''} ,
  ];


  for (let i = 0; i < end.length; i++) {
      tableFlasks.push(end[i]);
    };

  return(tableFlasks)
};


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
