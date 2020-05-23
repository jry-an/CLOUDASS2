function display_spanish_text() {
    var x = document.getElementById("spanish_text");
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }

  function myFunction() {
    var a = document.getElementById("myDropdown").classList.toggle("show");
    if (a.style.display === "none") {
      a.style.display = "block";
      var d = "DA"
    } else {
      a.style.display = "none";
    }
  }
  function filterFunction() {
    var input, filter, ul, li, a, i;
    input = document.getElementById("SearchBar");
    filter = input.value.toUpperCase();
    div = document.getElementById("Content");
    a = div.getElementsByTagName("a");
    for (i = 0; i < a.length; i++) {
      txtValue = a[i].textContent || a[i].innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        a[i].style.display = "";
      } else {
        a[i].style.display = "none";
      }
    }
  }
  
  document.querySelectorAll('.topbtn').forEach(function(item) {
    let getBtnData = item.dataset.button;
    item.addEventListener('click', function(e) {
      document.querySelector('[data-type="' + getBtnData + '"]').classList.toggle('visibility')
    })
  
  })