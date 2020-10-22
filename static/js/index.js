var loadFile = function(event) {
        var data = new Image();
        var a = document.createElement('h5');
        data.src =  URL.createObjectURL(event.target.files[0])
        a.innerHTML = event.target.files[0].name
        data.classList.add('hide')
        a.setAttribute("id", event.target.files[0].name);
        data.setAttribute("id", 'Img-'+event.target.files[0].name);
        // a.setAttribute("onclick", "showHide(event)");

        var view = document.createElement('i');
        view.setAttribute("aria-hidden", "true");
        view.classList.add("fa");
        view.classList.add("fa-eye");
        view.setAttribute("id",event.target.files[0].name);
        view.setAttribute("onclick", "showHide(event)");
        a.appendChild(view);

        // <a href="/images/myw3schoolsimage.jpg" download>


        var downloadIcon = document.createElement('i');
        downloadIcon.setAttribute("aria-hidden", "true");
        downloadIcon.classList.add("fa");
        downloadIcon.classList.add("fa-download");
        // a.appendChild(downloadIcon);

        var imgDownload = document.createElement('a');
        // imgDownload.innerHTML = 'Down'
        imgDownload.setAttribute('href',event.target.files[0].name)
        imgDownload.setAttribute('download',event.target.files[0].name)
        imgDownload.classList.add('add-icon')
        a.appendChild(imgDownload);
        // imgDownload.appendChild(downloadIcon);



        document.getElementById('temp').appendChild(a);
        document.getElementById('temp').appendChild(data);
        imgDownload.appendChild(downloadIcon);
        console.log("======>>>",event.target.files)

    };

var showHide = function(event){
     console.log("====>>>",event.target.id)
     var ele = document.getElementById('Img-'+event.target.id)
     if(ele.classList.contains("hide")){
        ele.classList.remove("hide");
        ele.classList.add("show");
     }else{
        ele.classList.remove("show");
        ele.classList.add("hide");
     }
}

let is_typing = false
let roomName = "test"

var Socket = roomName ? new WebSocket(
            'ws://' + window.location.host +
            '/ws/' + roomName + '/') : new WebSocket(
            'ws://' + window.location.host +
            '/ws/')

Socket.onmessage = function(e) {
            var data = JSON.parse(e.data);
            let data_element = document.getElementById("message")
            switch(data.category){
                case "ALL_DATA":
                    var message = JSON.parse(data.data);
                    console.log("message : ", message)
                    data_element.value = message.clipboard_data
                    session_id = data.session_id
                    private_name = data.private_name
                    sessionStorage.setItem("session_id", session_id)
                    sessionStorage.setItem("private_name", private_name)
                    break;
                case "CLIPBOARD":
                    if(sessionStorage.getItem("private_name") != data.private_name){
                        data_element.value = data.data
                    }
                    break;
            }

        };


$("#message").on("input", function(event){
    let obj = JSON.stringify({"category":"CLIPBOARD", "data":$("#message").val(), "private_name": sessionStorage.getItem("private_name")})
    Socket.send(obj)
})


Socket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};



