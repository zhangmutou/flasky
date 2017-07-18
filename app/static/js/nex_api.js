// 复选框全选、反选
$(document).ready(function () {
  $('#checkall').click(function () {
    if ($(this).prop('checked')) {
      $('tbody :checkbox').prop('checked', true);
    } else {
      $('tbody :checkbox').prop('checked', false);
    }
  });
});

$(document).ready(function() {
  $('#exc-checked').click(function() {
    var case_values = new Array();
    // var origin_str = $('#alert').html();
    $("input[name='case']:checked").each(function() {
      case_values.push(this.value)
    });
    if (case_values.length == 0) {
      var result = confirm('请勾选需要执行的用例');
      if(result){
        return;
      } else {
        return;
      };
    };
    $(this).button('loading');
    $.post('/nex-api/exc', {
      ids: case_values
    },
    function(data) {
      console.log(data.msg);
      window.location.reload()
      // $('#exc-checked').button('reset');
    });
  });
});

$(document).ready(function() {
  $('#exc-all').click(function() {
    $(this).button('loading');
    $(this).button('reset');
    console.log(3333);
    // setTimeout(function() { $(this).button('reset'); },1000);
  });
});

$(document).ready(function() {
  $('#save-modal').click(function() {
    clear_modal_data();
  });
});

$(document).ready(function() {
  $('#close-modal').click(function() {
    clear_modal_data();
  });
});

$(document).ready(function() {
  $('#close-show-modal').click(function() {
    clear_show_modal();
  });
});

function show_case(obj){
  var id = $(obj).attr("value");
  $.getJSON($SCRIPT_ROOT + '/nex-api/get', {
    id: id
  },
  function(data) {
    console.log(data.msg);
      var s1 = eval('(' + data.msg['request_data'] + ')');
      var s2 = eval('(' + data.msg['expectation'] + ')');
      var req_data = library.json.prettyPrint(s1);
      var req_expc = library.json.prettyPrint(s2);
      $("#request-data").html(req_data);
      $("#request-url").html(data.msg['url']);
      $("#request-desc").html(data.msg['desc']);
      $("#request-type").html(data.msg['request_type']);
      $("#request-expection").html(req_expc);
      $("#request-name").html(data.msg['name']);
      $("#request-id").html(data.msg['id']);
    // });
  });
};

function update_case(obj){
  var id = $(obj).attr("value");
  $.getJSON($SCRIPT_ROOT + '/nex-api/get', {
    id: id
  },
  function(data) {
    console.log(data.msg);
    $('#update-id').val(data.msg['id']);
    $('#update-name').val(data.msg['name']);
    $('#update-url').val(data.msg['url']);
    $('#update-desc').val(data.msg['desc']);
    $('#update-data').val(data.msg['request_data']);
    $('#update-expectation').val(data.msg['expectation']);
    if (data.msg['request_type']=='post') {
      // $('#update-post').checked=true;
      document.getElementById('update-post').checked = true;
    } else {
      document.getElementById('update-get').checked = true;
    };
  });
};

function clear_modal_data(){
  $('#new').on('hidden.bs.modal', function () {
    $('#add-name').val('');
    $('#add-desc').val('');
    $('#add-url').val('');
    $('#add-data').val('');
    $('#add-expectation').val('');
    document.getElementById('add-post').checked = false;
    document.getElementById('add-get').checked = false;
  });
};

function clear_show_modal(){
  $('#show').on('hidden.bs.modal', function() {
    $('#request-id').empty();
    $('#request-url').empty();
    $('#request-name').empty();
    $('#request-desc').empty();
    $('#request-type').empty();
    $('#request-expection').empty();
    $('#request-data').empty();
    $('#response-data').empty();
    $('#awaiting').html('Awaiting request...');
  });
};

function edit_case(obj){
  var id = $('#update-id').val();
  var name = $('#update-name').val();
  var desc = $('#update-desc').val();
  var curl = $('#update-url').val();
  var data = $('#update-data').val();
  var expectation = $('#update-expectation').val();
  if ($('#update-post :checked')) {
    var type = 'post'
  };
  if ($('#update-post :checked')) {
    var type = 'get'
  };
  $.post('/nex-api/update', {
    id: id,
    name: name,
    desc: desc,
    curl: curl,
    data: data,
    type: type,
    expectation: expectation
    },
    function(data) {
      alert(data.msg);
  });
};

function add_case(){
  // var data = $('#new').data();
  var name = $('#add-name').val();
  var desc = $('#add-desc').val();
  var curl = $('#add-url').val();
  var data = $('#add-data').val();
  var expectation = $('#add-expectation').val();
  if ($('#add-post :checked')) {
    var type = 'post';
  } else if ($('#add-post :checked')) {
    var type = 'get';
  } else {
    var type = '';
  };
  if (!type) {
    console.log('dfddf');
  };
  // console.log(data);
  if (!name || !desc || !curl || !data || !expectation || !type) {
    var result = confirm('不允许为空');
    if(result){
        return false;
    }else{
        return false;
    }
  };
  $.post('/nex-api/add', {
    name: name,
    desc: desc,
    curl: curl,
    data: data,
    type: type,
    expectation: expectation
    },
    function(data) {
      alert(data.msg);
  });
};

function send_case(obj){
  var id = $('#request-id').text();
  // var case_data = $('#request-data').text();
  $.post('/nex-api/send', {
    id: id
  },
  function(data) {
    $('#awaiting').empty();
    var data = library.json.prettyPrint(data.msg);
    console.log(data);
    $('#response-data').html(data);
  });
};

function del_case(obj){
  var id = $(obj).attr("value");
  $.post('/nex-api/delete', {
    id: id
  },
  function(data) {
    alert(data.msg);
  });
};

function del_confirm(obj){
    var result = confirm('删除后无法恢复，请谨慎操作');
    if(result){
        del_case(obj);
    }else{
        return false;
    }
};

function sleep(d){
  for(var t = Date.now();Date.now() - t <= d;);
};

if (!library)
   var library = {};
library.json = {
  replacer: function(match, pIndent, pKey, pVal, pEnd) {
    var key = '<span class=json-key>';
    var val = '<span class=json-value>';
    var str = '<span class=json-string>';
    var r = pIndent || '';
    if (pKey)
       r = r + key + pKey.replace(/[": ]/g, '') + '</span>: ';
    if (pVal)
       r = r + (pVal[0] == '"' ? str : val) + pVal + '</span>';
    return r + (pEnd || '');
  },
  prettyPrint: function(obj) {
    var jsonLine = /^( *)("[\w]+": )?("[^"]*"|[\w.+-]*)?([,[{])?$/mg;
    return JSON.stringify(obj, null, 3)
       .replace(/&/g, '&amp;').replace(/\\"/g, '&quot;')
       .replace(/</g, '&lt;').replace(/>/g, '&gt;')
       .replace(jsonLine, library.json.replacer);
  }
};