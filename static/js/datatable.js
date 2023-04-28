function addFilter(){
  let filter = document.getElementById("datatable_filter");
  var filterButton = $('<div class="filter-button" onclick="toggleFilter()">Lọc</div>').appendTo(filter);
  
  var tags = ["Laptop", "Chuột", "Bàn phím", "Tai nghe", "Loa", "Mic", "Card đồ họa", "Pin", "Sạc", "USB", "Ram", "Ổ cứng", "Webcam"];
  var idTags = ["laptop", "mouse", "keyboard", "headphone", "loudspeaker", "mic", "vga", "battery", "charger", "usb", "ram", "harddisk", "webcam"];

  var brands = ["Dell", "Mac", "MSI", "ASUS", "Lenovo", "Intel", "ACER", "HP", "Logitech"];
  var idBrands = ["Dell", "Mac", "MSI", "ASUS", "Lenovo", "Intel", "ACER", "HP", "Logitech"];

  var shops = ["Phong Vũ", "Thế giới di dộng", "GearVN", "CellphoneS"];
  var idShops = ["phongvu", "thegioididong", "gearvn", "cellphones"];

  var filterDiv = $('<div class="filter"></div>').appendTo(filter);
  var tagDiv = $('<div class="filter-tag filter-section"></div>').appendTo(filterDiv);
  var brandDiv = $('<div class="filter-brand filter-section"></div>').appendTo(filterDiv);
  var shopDiv = $('<div class="filter-shop filter-section" style="display: block;"></div>').appendTo(filterDiv);

  $('<label style="width: 100%"><strong>Loại sản phẩm</strong></label>').appendTo(tagDiv);
      

  var allItemDiv1 = $('<div class="check-div"></div>').appendTo(tagDiv);
  $('<input type="checkbox" name="item-category" checked>')
    .attr('id', 'all-item-category')
    .attr('value', 'all')
    .appendTo(allItemDiv1);
  $('<label></label>')
    .attr('for', 'all-item-category')
    .text('Tất cả')
    .appendTo(allItemDiv1);
  
  for (var i = 0; i < tags.length; i++) {
    var tag = tags[i];
    var idTag = idTags[i];
    var checkDiv = $('<div class="check-div"></div>').appendTo(tagDiv);
    
    $('<input type="checkbox" name="item-category" class="item-category">')
    .attr('id', idTag)
    .attr('value', tag)
    .appendTo(checkDiv);
    
    $('<label></label>')
    .attr('for', idTag)
    .text(tag)
    .appendTo(checkDiv);
  }


  $('<label style="width: 100%"><strong>Hãng sản xuất</strong></label>').appendTo(brandDiv);

  var allItemDiv2 = $('<div class="check-div"></div>').appendTo(brandDiv);
  $('<input type="checkbox" name="item-brand" checked>')
    .attr('id', 'all-item-brand')
    .appendTo(allItemDiv2);
  $('<label></label>')
    .attr('for', 'all-item-brand')
    .text('Tất cả')
    .appendTo(allItemDiv2);
        
  for (var i = 0; i < brands.length; i++) {
    var tag = brands[i];
    var idTag = idBrands[i];
    var checkDiv = $('<div class="check-div"></div>').appendTo(brandDiv);
    var checkbox = $('<input type="checkbox" name="item-brand" class="item-brand">')
    .attr('id', idTag)
    .attr('value', tag)
    .appendTo(checkDiv);
    var label = $('<label></label>')
    .attr('for', idTag)
    .text(tag)
    .appendTo(checkDiv);
  }

  $('<label style="width: 100%"><strong>Cửa hàng</strong></label>').appendTo(shopDiv);

  var allItemDiv3 = $('<div class="check-div"></div>').appendTo(shopDiv);
  $('<input type="checkbox" name="item-shop" checked>')
    .attr('id', 'all-item-shop')
    .appendTo(allItemDiv3);
  $('<label></label>')
    .attr('for', 'all-item-shop')
    .text('Tất cả')
    .appendTo(allItemDiv3);
        
  for (var i = 0; i < shops.length; i++) {
    var tag = shops[i];
    var idTag = idShops[i];
    var checkDiv = $('<div class="check-div"></div>').appendTo(shopDiv);
    var checkbox = $('<input type="checkbox" name="item-shop" class="item-shop">')
    .attr('id', idTag)
    .attr('value', tag)
    .appendTo(checkDiv);
    var label = $('<label></label>')
    .attr('for', idTag)
    .text(tag)
    .appendTo(checkDiv);
  }

  
  var rangeInput = $(
    '<table class="inputs">' + 
      '<tbody>' + 
        '<tr>' +
          '<td colspan="2" style="text-align: left;"><strong>Mức giá</strong></td>' +
        '</tr>' +
        '<tr>' +
          '<td colspan="2" style="text-align: left;">' + 
            '<input type="checkbox" name="item-sale" id="item-sale" value="Đang giảm giá">' + 
            '<lable for="item-sale">Đang giảm giá</lable>' +
          '</td>' +
        '</tr>' +
        '<tr>' +
          '<td colspan="2" style="text-align: left;" onclick="priceClick(0, 10000000)">Dưới 10 triệu</td>' +
        '</tr>' +
        '<tr>' +
          '<td colspan="2" style="text-align: left;" onclick="priceClick(10000000, 15000000)">Từ 10 - 15 triệu</td>' +
        '</tr>' +
        '<tr>' +
          '<td colspan="2" style="text-align: left;" onclick="priceClick(15000000, 20000000)">Từ 15 - 20 triệu</td>' +
        '</tr>' +
        '<tr>' +
          '<td colspan="2" style="text-align: left;" onclick="priceClick(20000000, 25000000)">Từ 20 - 25 triệu</td>' +
        '</tr>' +
        '<tr>' +
          '<td colspan="2" style="text-align: left;" onclick="priceClick(25000000)">Trên 25 triệu</td>' +
        '</tr>' +
        '<tr style="border-top: 1px #fff dashed;">' +
          '<td style="float: left;">Giá thấp nhất:</td>' +
          '<td><input type="text" id="min" name="min"></td>' +
        '</tr>' +
        '<tr>' +
          '<td style="float: left;">Giá cao nhất:</td>' +
          '<td><input type="text" id="max" name="max"></td>' +
        '</tr>' +
      '</tbody>' +
    '</table>'
  ).appendTo(filterDiv);
}

$(document).ready( function () {
  $.getJSON( "./data", function( data ) {

    let table = $('#datatable').DataTable({
      language: {
        search:"",
      },
      dom: 'frtp',
      data: data,
      select:"single",
      columns: [
        {
          "className": 'details-control',
          "orderable": false,
          "data": null,
          "defaultContent": '',
          "render": function () {
            return '<i class="fa fa-plus-square" aria-hidden="true"></i>';
          },
          width:"15px"
        },
        {
          "data": "img",
          "render": function ( data, type, row ) {
            return '<img src="' + data + '"/>';
          },
          "searchable": false,
          "className": 'item-image item-column'
        },
        {
          "data" : "brand",
          "className": 'item-column'
        },
        {
          "data" : "name",
          "className": 'item-name item-column'
        },
        {
          "data" : "curPrice",
          // "searchable": false,
          "className": 'item-curPrice item-column'
        },
        {
          "data": "curPrice1", 
          "visible": false,
          // "searchable": false,
          "className": 'item-curPrice1 item-column'
        },
        {
          "data": "tag", 
          "visible": false,
          "className": 'item-tag item-column'
        },
        {
          "data": "isSale", 
          "visible": false,
          // "searchable": false,
          "className": 'item-sale item-column'
        },
        {
          "data": "shopName", 
          "visible": false,
          // "searchable": false,
          "className": 'item-shopName item-column'
        },
      ],
      "columnDefs": [
        { "width": "20%", "targets": 1, "orderable": false},
        { "width": "10%", "targets": 2, "render": $.fn.dataTable.render.text(), "white-space": "normal", "style": "text-align: center;" },
        { "width": "50%", "targets": 3, "render": $.fn.dataTable.render.text(), "white-space": "normal"},
        { "width": "20%", "targets": 4, "style": "text-align: center;", "orderData": [ 5 ] }, 
      ],
      "order": [[3, 'asc']]
    });

    
    // search section
    $('[type=search]').each(function() {
      $(this).attr("placeholder", "Search...");
      $(this).before('<span class="fa fa-search"></span>');
      $(this).attr("id", "search-box");
    });
    
    addFilter();
    
// SELECT ALL IMPLEMENTATION
    $('.item-category').click(function() {
      if ($('.item-category:not(:checked)').length === 0) {
        $('#all-item-category').prop('checked', true);
      } else {
        $('#all-item-category').prop('checked', false);
      }
    });
    
    $('#all-item-category').click(function() {
      if ($(this).prop('checked')) {
        $('.item-category').prop('checked', true);
      } else {
        $('.item-category').prop('checked', false);
      }
    });


    $('.item-brand').click(function() {
      if ($('.item-brand:not(:checked)').length === 0) {
        $('#all-item-brand').prop('checked', true);
      } else {
        $('#all-item-brand').prop('checked', false);
      }
    });
    
    $('#all-item-brand').click(function() {
      if ($(this).prop('checked')) {
        $('.item-brand').prop('checked', true);
      } else {
        $('.item-brand').prop('checked', false);
      }
    });


    $('.item-shop').click(function() {
      if ($('.item-shop:not(:checked)').length === 0) {
        $('#all-item-shop').prop('checked', true);
      } else {
        $('#all-item-shop').prop('checked', false);
      }
    });
    
    $('#all-item-shop').click(function() {
      if ($(this).prop('checked')) {
        $('.item-shop').prop('checked', true);
      } else {
        $('.item-shop').prop('checked', false);
      }
    });


    // Add event listener for opening and closing details
    $('#datatable tbody').on('click', 'td.details-control', function () {
      var tr = $(this).closest('tr');
      var tdi = tr.find("i.fa");
      var row = table.row(tr);

      if (row.child.isShown()) {
        // This row is already open - close it
        row.child.hide();
        tr.removeClass('shown');
        tdi.first().removeClass('fa-minus-square');
        tdi.first().addClass('fa-plus-square');
      }
      else {
        // Open this row
        row.child(format(row.data())).show();
        tr.addClass('shown');
        tdi.first().removeClass('fa-plus-square');
        tdi.first().addClass('fa-minus-square');
      }
    });

    table.on("user-select", function (e, dt, type, cell, originalEvent) {
      if ($(cell.node()).hasClass("details-control")) {
        e.preventDefault();
      }
    });
  });

  waitAndSelectElement().then(function(element) {
    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) { 
      var min = parseInt(element[0].val(), 10);
      var max = parseInt(element[1].val(), 10);
      var checkedCategoryBoxes = element[2].filter(':checked');
      var checkedBrandBoxes = element[3].filter(':checked');
      var checkedShopBoxes = element[4].filter(':checked');
      var saleBox = element[5];
      
      var price = parseFloat(data[5]) || 0; // use data for the price column
      var tag = data[6];
      var brand = data[2];
      var shop = data[8];
      var isSale = data[7];
      if (
        (
          (
            (isNaN(min) && isNaN(max)) ||
            (isNaN(min) && price <= max) ||
            (min <= price && isNaN(max)) ||
            (min <= price && price <= max)
          ) 
          &&
          (
            checkEqual("all-item-category", checkedCategoryBoxes) ||checkEqual(tag, checkedCategoryBoxes)
          )
          &&
          (
            checkEqual("all-item-brand", checkedBrandBoxes) || checkEqual(brand, checkedBrandBoxes)
          )
          &&
          (
            checkEqual("all-item-shop", checkedShopBoxes) || checkEqual(shop, checkedShopBoxes)
          )
          &&
          (
            !saleBox.is(":checked") || (isSale == 1)
          )
        )
      ) {
        return true;
      }
      return false;
    });
    
    // Changes to the inputs will trigger a redraw to update the table
    element[0].on('input', function () {
      $('#datatable').DataTable().draw();
    });
    element[1].on('input', function () {
      $('#datatable').DataTable().draw();
    });
    element[2].each(function(){
      $(this).on('change', function(){
        $('#datatable').DataTable().draw();
      })
    })
    element[3].each(function(){
      $(this).on('change', function(){
        $('#datatable').DataTable().draw();
      })
    })
    element[4].each(function(){
      $(this).on('change', function(){
        $('#datatable').DataTable().draw();
      })
    })
    element[5].on('change', function(){
      $('#datatable').DataTable().draw();
    })

  }).catch(function(error) {
    // Handle the error
    console.error(error);
  });

});


function waitAndSelectElement() {
  return new Promise(function(resolve, reject) {
    // Call the other function that needs to run first

    setTimeout(function() {
      // Select the element by ID
      var minEl = $('#min');
      var maxEl = $('#max');
      var categoryEls = $('input[name="item-category"]');
      var brandEls = $('input[name="item-brand"]');
      var shopEls = $('input[name="item-shop"]');
      var saleEl = $('input[name="item-sale"]');

      // Check if the element exists
      if (minEl.length > 0 && maxEl.length > 0 && categoryEls.length > 0) {
        // If the element exists, resolve the promise with the element
        resolve([minEl, maxEl, categoryEls, brandEls, shopEls, saleEl]);
      } else {
        // If the element doesn't exist, reject the promise with an error message
        reject("Element not found");
      }
    }, 1000);
  });
}

function format(d){

  let oriPriceDiv = (d.oriPrice == "") ? "" : d.oriPrice + "  (-" + d.discount + "%)";
  systemDiv = "";
  if (d.system == "") {
    systemDiv = "";
  }
  else {
      (d.system).forEach(item => systemDiv = systemDiv + "<p>" + item + "</p>")
  }
  // `d` is the original data object for the row
  return '<table class="extra-infor" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">' +
    '<tr>' +
    '<td>Tên trang web:</td>' +
    '<td>' + d.shopName1 + '</td>' +
    '</tr>' +
    '<tr>' +
    '<td>Cấu hình:</td>' +
    '<td>' + systemDiv + '</td>' +
    '</tr>' +
    '<tr>' +
    '<td>Giá gốc:</td>' +
    '<td>' + oriPriceDiv + '</td>' +
    '</tr>' +
    '<tr>' +
    '<td>URL:</td>' +
    '<td><a href="' + d.url + '">Link sản phẩm</a></td>' +
    '</tr>' + 
    '</table>';   
}

function checkEqual(tag, EleArr){
  let check = 0;
  EleArr.each(function(){
    if(tag.toLowerCase().localeCompare($(this).attr("id").toLowerCase()) == 0) {
        check++;
        return false;
    }
  })
  if(check) return true;
  else return false;
}

function priceClick(min, max){
  $('#min').val(min).trigger('input');
  $('#max').val(max).trigger('input');
}

function toggleFilter(){
  let filterDiv = document.querySelector(".filter");
  // let filterTag = document.querySelector(".filter-tag");
  filterDiv.classList.toggle("appear");
}