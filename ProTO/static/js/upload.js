$(document).ready(function () {
  $("#video").change(function () {
    call();
  });
});
var video;

function call() {
  var file_Selected = document.getElementById("video");
  file_Selected_file = file_Selected.files[0];
  var fileUrl = window.URL.createObjectURL(file_Selected_file);
  var obj = document.getElementById("video2");
  obj.style.visibility = "visible";
  obj.src = fileUrl;
}
var initialize = function () {
  $("#capture").click(captureImage);
};

var captureImage = function () {
  video = $("#video2").get(0);
  var canvas = document.createElement("canvas");
  canvas.width = 330;
  canvas.height = 200;

  canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
  var out = document.getElementById("output2");
  out.value = canvas.toDataURL();
};
initialize();

const file_vd = document.getElementById("video");
const progress_bar = document.getElementsByClassName("progress-bar-filler")[0];

const progress_text = document.getElementsByClassName("progress-bar-text")[0];

function submitVDFORM(e) {
  e.preventDefault();
  let vdform = document.getElementById("videoform");
  var token = $("input[name=csrfmiddlewaretoken]").val();
  let caption = document.getElementById("id_captions").value;
  let vd_file = document.getElementById("video");
  //let file_Selecteds=document.getElementById('video');
  let thubimg = document.getElementById("output2").value;

  let eventsname = document.getElementById("E").value;
  //console.log(eventsname);

  let formsdata = new FormData();
  formsdata.append("csrfmiddlewaretoken", token);
  formsdata.append("captions", caption);
  formsdata.append("video", vd_file.files[0]);
  formsdata.append("thumbnail", thubimg);
  formsdata.append("events",eventsname);

  formTask = $.ajax({
    xhr: function () {
      var xhr = new window.XMLHttpRequest();
      xhr.upload.addEventListener(
        "progress",
        function (evt) {
          let percentComplete = 0;
          if (evt.lengthComputable) {
            percentComplete = (evt.loaded / evt.total) * 100;

          } else percentComplete = 0;

          progress_bar.style.width = percentComplete.toFixed(2) + "%";
          progress_text.textContent = percentComplete.toFixed(1) + "%";
        },
        false
      );
      return xhr;
    },

    type: "POST",
    url: "/upload/ajax",

    //contentType: 'multipart/form-data',

    enctype: "multipart/form-data",
    data: formsdata,
    success: function (respone) {
      alert(" FILE UPLOADED ");
       vdform.reset();
         percentComplete = 0;
        progress_bar.style.width = percentComplete.toFixed(2) + "%";
        progress_text.textContent = percentComplete.toFixed(1) + "%";

    },
    error: function (error) {
      alert(error.responseJSON.video);
    },

    cache: false,
    contentType: false,
    processData: false,
  });

  return false;
}