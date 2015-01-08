(function ($) {
  $(document).ready(function () {
    $('.form-editrole').change(function () {
      var id = $(this).attr('id').split('_')[2];
      var value = $(this).children('select').val();
      $.ajax({
        url: document.location.pathname, // the endpoint
        type: "POST", // http method
        data: { id: id, value: value}, // data sent with the post request

        // handle a successful response
        success: function (json) {
          var role_names = json.role_names
            , role = json.role
            , user_id = json.user_id;
          $('.user-' + user_id + ' .user-role').html(role_names[role]);
          $('#post-text').val(''); // remove the value from the input
          console.log(json); // log the returned json to the console
          console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error: function (xhr, errmsg, err) {
          $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
            " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
      });
    });

    $('.add-task, .edit-group').click(function (e) {
      var that = this;
      e.preventDefault()
      var link = $(this).attr('href');
      $.ajax({
        url: link,
        success: function (response) {
          var new_content = /*$('.project-info').append(response);//*/$(that).parents('tr').find('.add-task-form').append(response);
          $('.modal', new_content).modal();
          $('.modal', new_content).on('hidden.bs.modal', function () {
            $(this).remove();
          });
          $($(new_content).find('form')).on('submit', Form.handlers[$(new_content).find('form').attr('id').replace(/-/g, '_')]);
        },
        error: function (xhr, errmsg, err) {
          $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
            " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
      })
    });

    //$('#add-task-form').live(function() {

    //});

    // This function gets cookie with a given name
    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    /*
     The functions below will create a header with csrftoken
     */

    function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
      // test that a given url is a same-origin URL
      // url could be relative or scheme relative or absolute
      var host = document.location.host; // host + port
      var protocol = document.location.protocol;
      var sr_origin = '//' + host;
      var origin = protocol + sr_origin;
      // Allow absolute or scheme relative URLs to same origin
      return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
      beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
          // Send the token to same-origin, relative URLs only.
          // Send the token only if the method warrants CSRF protection
          // Using the CSRFToken value acquired earlier
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });
  })

  /**
   * Form class
   * @constructor
   */
  var Form = function () {};
  Form.handlers = {};

  /**
   * Submit handler for add task form
   */
  Form.handlers.add_task_form = function (e) {
    e.preventDefault();
    var values = {};
    var that = this;
    var link = $(this).attr('action');
    $(this).find(':input').each(function (item) {
      values[$(this).attr('name')] = $(this).val();
    });
    $(this).find('input[type="submit"]').addClass('disabled');
    $.ajax({
      url: link,
      type: 'POST',
      data: values,
      success: function (data, success) {
        if (data.success) {
          $(that).find('input[type="submit"]').removeClass('disabled');
          $('.group tbody').append('<tr><td>' + data.task + '</td></tr>');
          //$(that).parents('.add-task-form').parent().parent().append('<tr><td>' + data.task + '</td></tr>');
          $(that).parents('.modal').remove();
        }
        else {
          var errors = JSON.parse(data.errors);
          for (var error in errors) {
            $(that).find('.' + error).append('<div class="alert alert-danger">' + errors[error] + '</div>');
          }
          $(that).find('input[type="submit"]').removeClass('disabled');
        }
      }
    });
  };

  Form.handlers.edit_group_form = function (e) {
    e.preventDefault();
    var values = {}
      , that = this
      , link = $(this).attr('action');
    $(this).find(':input').each(function(item) {
      values[$(this).attr('name')] = $(this).val();
    });
    $(this).find('input[type="submit"]').addClass('disabled');
    $.ajax({
      url: link,
      type: 'POST',
      data: values,
      success: function (data, success) {
        if (data.success) {
          $('.group-name').html(data.groupName);
          $(that).find('input[type="submit"]').removeClass('disabled');
          $(that).parents('.modal').remove();
        }
        else {
          var errors = JSON.parse(data.errors);
          alert(errors);
          $(that).find('input[type="submit"]').removeClass('disabled');
        }
      }
    });
  }

})(jQuery)