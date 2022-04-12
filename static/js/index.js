$( document ).ready(function() {

    var private_name = null;
    var session_id = null;
    var ws = new WebSocket("ws://127.0.0.1:8000/ws/")
    // JQuery Event
    $("#file").on("change", function(event){
        apiUploadFile(event)
    })

    $("#file-list").on("click", 'img', function(event){
        apiDeleteFile(event.target.id)
    })

    $('#toggle-two').bootstrapToggle({
      on: 'Detail View',
      off: 'List View'
    });

    ws.onopen = (event) => {
        toastr.success('You Connected Successfully', 'Success', {timeOut: 5000})
    };

    ws.onmessage = (event) => {
        var onMessageData = JSON.parse(event.data);
        console.log(onMessageData)
        switch(onMessageData.category){
            case "ALL_DATA":
                toastr.info('You Have All Data Now', 'Information', {timeOut: 5000})
                displayFiles(onMessageData.data.file_data)
                break
            case "FILE":
                toastr.success('Update File List', 'Success Alert', {timeOut: 5000})
                displayFiles(onMessageData.data)
                break
            case "CLIPBOARD":
                toastr.success('Text Updated', 'Success Alert', {timeOut: 50000})
                break
        }
        session_id = onMessageData.session_id;
        private_name = onMessageData.private_name;
    };

    let displayFiles = (fileList) => {
        $('#file-list').empty();
        fileList.forEach((item) => {
            $('#file-list').append(`<div class="col-md-4 " >
                <div class="card p-3 mb-2 card-shadow">
                    <div class="d-flex justify-content-between align-items-center">
                        <div class="d-flex flex-row align-items-center ">
                            <div class="icon"> <i class="fa fa-file-pdf-o" style="font-size:36px; color:#007bff;"></i> </div>
                            <div class="ms-2 c-details">
                                <h6 class="mb-0">${item.file}</h6> <span>${item.timestamp}</span>
                            </div>
                        </div>
                        <div class="badge">
                            <span>
                                <img  id=${item.id} src="../static/assets/delete.ico">
                            </span>
                        </div>
                    </div>
                </div>
            </div>`)
        })
    }

    let apiDeleteFile = (fileId) => {
        var settings = {
          "async": true,
          "crossDomain": true,
          "url": `/file/${fileId}`,
          "method": "DELETE",
          "headers": {
            "cache-control": "no-cache",
          },
          "processData": false,
          "contentType": false,
          success: function (response) {
            console.log("response : ", response);
            ws.send(JSON.stringify({
                "category":"FILE",
                "private_name": private_name,
                "message": "No-Content"
            }))
          },
          error: function (error) {
            console.log("error : ", error);
          }
        }
        $.ajax(settings)
    }

    let apiUploadFile = (event) => {
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
            ws.send(JSON.stringify({
                "category":"FILE",
                "private_name": private_name,
                "message": response.file
            }))
          },
          error: function (error) {
            console.log("error : ", error);
          }
        }

        $.ajax(settings)
    }

});

  