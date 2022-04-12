$( document ).ready(function() {
    function uploadFile(event){
        var form = new FormData();
        form.append("file", event.target.files[0]);

        var settings = {
          "async": true,
          "crossDomain": true,
          "url": "/file/",
          "method": "POST",
          "headers": {
            "cache-control": "no-cache",
          },
          "processData": false,
          "contentType": false,
          "mimeType": "multipart/form-data",
          "data": form,
          success: function (response) {
            console.log("response : ", response);
          },
          error: function (error) {
            console.log("error : ", error);
          }
        }

        $.ajax(settings)
    }


    $("#file").on("change", function(event){
         console.log('event:', event.target.files);
        uploadFile(event)
    })

});

$(function() {
    $('#toggle-two').bootstrapToggle({
      on: 'Detail View',
      off: 'List View'
    });
  })
  