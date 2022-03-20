const IC = '<i class="mdui-icon material-icons">account_circle</i>';
const IM = '<img class="mdui-img-circle mdui-center" src="/auth/head" style="height:32px;width:32px;"/>';

var info;

var $ = mdui.$;

function Head() {
  $.ajax({
    method: 'GET',
    url: '/auth/info',
    success: function (data) {
      info = JSON.parse(data);
      if ('uid' in info) {
        $("#account-ico").html(IM);
      } else {
        $("#account-ico").html(IC);
      }
    }
  });
}

Head();