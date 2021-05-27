$("#unseen").on("click", function () {
  $.ajax({
    type: "GET",
    url: "/moderator/ajax",
    data: {
      videos: "unseen",
    },
    success: function (respone) {
      document.getElementById("eventname").style.display = "none";
      document.getElementsByClassName("output")[0].style.display = "flex";
      document.getElementById("dia").style.display = "none";
      document.getElementById("infoteller").innerHTML = "PENDING ";
      let responeObject = respone.data;
      let tb = document.getElementById("TB");
      tb.innerHTML = "";
      let upd = document.getElementById("UPD");
      upd.innerHTML = "UPLOADED DATE";
      for (i in responeObject) {
        let tr = document.createElement("tr");
        let link = responeObject[i].url_64encoding;
        let date = responeObject[i].date;
        let uploadeduser = responeObject[i].username;
        let tdtemp = document.createElement("td");
        tr.appendChild(tdtemp);
        for (let j = 0; j < 3; j++) {
          let td = document.createElement("td");
          if (j === 0) {
            let a = document.createElement("a");
            a.setAttribute("href", "/videos/" + link);
            a.setAttribute("target", "_blank");
            a.innerHTML = "LINK";
            td.appendChild(a);
          }
          if (j === 1) {
            td.innerHTML = date;
          }
          if (j === 2) {
            td.innerHTML = uploadeduser;
          }

          tr.appendChild(td);
        }
        tb.appendChild(tr);
      }
    },
  });
});

$("#verified").on("click", function () {
  $.ajax({
    type: "GET",
    url: "/moderator/ajax",
    data: {
      videos: "verified",
    },
    success: function (respone) {
      let responeObject = respone.data;
      //document.getElementById("eventname").style.display = "none";
      document.getElementById("eventname").style.display = "table-cell";
      document.getElementById("eventname").innerHTML = "Marks";
      document.getElementsByClassName("output")[0].style.display = "flex";
      document.getElementById("dia").style.display = "none";
      document.getElementById("infoteller").innerHTML = " MODERATED ";
      let tb = document.getElementById("TB");
      tb.innerHTML = "";
      let upd = document.getElementById("UPD");
      upd.innerHTML = "DATE";
      for (i in responeObject) {
        let tr = document.createElement("tr");
        let link = responeObject[i].video_link;
        let date = responeObject[i].date;
        let uploadeduser = responeObject[i].by_email;
        let marks = responeObject[i].marks;
        let tdtemp = document.createElement("td");
        tr.appendChild(tdtemp);

        for (let j = 0; j < 4; j++) {
          let td = document.createElement("td");
          if (j === 0) {
            td.innerHTML = marks;
          }
          if (j === 1) {
            let a = document.createElement("a");
            a.setAttribute("href", "/videos/" + link);
            a.setAttribute("target", "_blank");
            a.innerHTML = "LINK";
            td.appendChild(a);
          }
          if (j === 2) {
            td.innerHTML = date;
          }
          if (j === 3) {
            td.innerHTML = uploadeduser;
          }

          tr.appendChild(td);
        }
        tb.appendChild(tr);
      }
    },
  });
});

$("#filterbyevent").on("click", function () {
  $.ajax({
    type: "GET",
    url: "/events/",
    success: function (respone) {
      let responeObject = respone.data;

      document.getElementById("eventname").style.display = "table-cell";
      document.getElementsByClassName("output")[0].style.display = "flex";
      document.getElementById("dia").style.display = "none";
      document.getElementById("infoteller").innerHTML =
        "SORT BY EVENTS PENDING VIDEOS ";
      document.getElementById('infoteller').style.fontSize="18px"

      let tb = document.getElementById("TB");
      tb.innerHTML = "";
      let upd = document.getElementById("UPD");
      upd.innerHTML = "DATE";
      for (i in responeObject) {
        let tr = document.createElement("tr");
        let link = responeObject[i].url_64encoding;
        let date = responeObject[i].date;
        let uploadeduser = responeObject[i].username;
        let eventsname = responeObject[i].EventName;
        let tdtemp = document.createElement("td");
        tr.appendChild(tdtemp);

        for (let j = 0; j < 4; j++) {
          let td = document.createElement("td");

          if (j === 1) {
            let a = document.createElement("a");
            a.setAttribute("href", "/videos/" + link);
            a.setAttribute("target", "_blank");
            a.innerHTML = "LINK";
            td.appendChild(a);
          }
          if (j === 0) {
            td.innerHTML = eventsname;
          }
          if (j === 2) {
            td.innerHTML = date;
          }
          if (j === 3) {
            td.innerHTML = uploadeduser;
          }

          tr.appendChild(td);
        }
        tb.appendChild(tr);
      }
    },
  });
});

$("#analytics").on("click", () => {
  $.ajax({
    type: "GET",
    url: "/analaytics/",
    success: function (respone) {
      document.getElementsByClassName("output")[0].style.display = "none";
      document.getElementById("dia").style.display = "flex";
      document.getElementById(
        "diag"
      ).innerHTML = `<canvas id="statcPie" ></canvas>`;
      let diag = document.getElementById("statcPie").getContext("2d");

      const data = {
        labels: ["CORRECTED ", "PENDING"],

        datasets: [
          {
            label: "My First Dataset",
            data: [respone.Actual_corrected, respone.Left_count],
            backgroundColor: ["rgb(255, 99, 132)", "rgb(54, 162, 235)"],
            hoverOffset: 4,
            options: {
              responsive: true,
              maintainAspectRatio: false,
              layout: {
                padding: 20,
              },
            },
          },
        ],
      };

      const config = {
        type: "pie",
        data: data,
      };

      let myChart = new Chart(diag, config);
    },
  });
});
