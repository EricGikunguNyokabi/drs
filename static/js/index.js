  //TOGGLE PASSWORD VISIBILITY =================================================================================
        //this function will be used in all login/registration pages where the id="myPassword" 
        function myFunction(){
          var x = document.getElementById("myPassword");
          var y = document.getElementById("myPassword2");
      
          if (x.type === "password" ){
              x.type = "text";
              y.type = "text";
          } else {
              x.type = "password";
              y.type = "password";
          }
      }
  //ENDOF TOGGLE PASSWORD VISIBILITY ==============================================================================
//==================================================================================================================
//==================================================================================================================
//Below script is used in co_centerredirect.html
    //array of constituencies for each county
const countyConstituencies = {
    "Nairobi": ["Westlands", "Kasarani", "Starehe", "Lang'ata", "Embakasi West", "Embakasi South", "Kamukunji", "Embakasi North", "Embakasi Central", "Dagoretti North", "Dagoretti South", "Makadara", "Mathare", "Ruaraka", "Kibra"],
    "Mombasa": ["Changamwe", "Jomvu", "Kisauni", "Nyali", "Likoni", "Mvita"],
    "Kwale": ["Msambweni", "Lunga Lunga", "Matuga", "Kinango"],
    "Kilifi": ["Kilifi North", "Kilifi South", "Kaloleni", "Rabai", "Ganze", "Malindi", "Magarini"],
    "Tana River": ["Bura", "Galole", "Garsen"],
    "Lamu": ["Lamu East", "Lamu West"],
    "Taita-Taveta": ["Taveta", "Wundanyi", "Mwatate"],
    "Garissa": ["Lagdera", "Dadaab", "Fafi", "Balambala", "Garissa Township"],
    "Wajir": ["Wajir North", "Wajir West", "Wajir East", "Tarbaj", "Eldas"],
    "Mandera": ["Mandera West", "Mandera North", "Mandera South", "Banissa", "Lafey"],
    "Marsabit": ["Laisamis", "North Horr", "Saku", "Moyale"],
    "Isiolo": ["Isiolo North", "Isiolo South"],
    "Meru": ["Igembe South", "Igembe North", "Igembe Central", "Tigania East", "Tigania West", "North Imenti", "Buuri", "Central Imenti", "South Imenti"],
    "Tharaka-Nithi": ["Maara", "Chuka/Igambang'ombe", "Tharaka"],
    "Embu": ["Manyatta", "Runyenjes", "Mbeere South", "Mbeere North"],
    "Kitui": ["Mwingi West", "Mwingi Central", "Mwingi North", "Kitui West", "Kitui Rural", "Kitui Central", "Kitui East"],
    "Machakos": ["Masinga", "Yatta", "Kangundo", "Matungulu", "Kathiani", "Mavoko", "Machakos Town", "Mwala"],
    "Makueni": ["Kilome", "Kaiti", "Kibwezi West", "Kibwezi East", "Mbooni"],
    "Nyandarua": ["Kinangop", "Kipipiri", "Ol Kalou", "Ol Joro Orok", "Ndaragwa"],
    "Nyeri": ["Tetu", "Kieni", "Mathira", "Othaya", "Mukurweini", "Nyeri Town", "Nyeri South"],
    "Kirinyaga": ["Mwea", "Gichugu", "Ndia", "Kirinyaga Central"],
    "Murang'a": ["Kangema", "Mathioya", "Kiharu", "Kigumo", "Maragua", "Kandara", "Gatanga"],
    "Kiambu": ["Gatundu South", "Gatundu North", "Juja", "Thika Town", "Ruiru", "Githunguri", "Kiambaa", "Kiambu Town", "Kabete", "Kikuyu", "Limuru", "Lari"],
    "Turkana": ["Turkana North", "Turkana West", "Turkana Central", "Loima", "Turkana South", "Turkana East"],
    "West Pokot": ["Kapenguria", "Sigor", "Kacheliba", "Pokot South", "Pokot Central"],
    "Samburu": ["Samburu West", "Samburu North", "Samburu East"],
    "Trans-Nzoia": ["Kwanza", "Endebess", "Saboti", "Kiminini", "Cherang'any"],
    "Uasin Gishu": ["Soy", "Turbo", "Moiben", "Ainabkoi", "Kapseret"],
    "Elgeyo-Marakwet": ["Kibwezi East", "Kilome", "Makueni", "Kaiti", "Mbooni", "Kilifi North", "Kilifi South", "Kaloleni", "Rabai", "Ganze", "Malindi", "Magarini"],
    "Nandi": ["Kinarani", "Kisauni", "Likoni", "Mvita", "Changamwe", "Jomvu", "Nyali", "Embakasi North", "Embakasi Central", "Embakasi South", "Embakasi West", "Embakasi East", "Makadara", "Kamukunji", "Starehe", "Mathare", "Westlands", "Dagoretti North", "Dagoretti South", "Lang'ata", "Kibra"],
    "Baringo": ["Moi's Bridge", "Soy", "Turbo", "Kapseret", "Kesses"],
    "Laikipia": ["Laikipia East", "Laikipia North", "Laikipia West"],
    "Nakuru": ["Nakuru East", "Nakuru West", "Nakuru North", "Nakuru South", "Rongai", "Subukia"],
    "Narok": ["Narok East", "Narok North", "Narok South", "Narok West"],
    "Kajiado": ["Kajiado Central", "Kajiado East", "Kajiado North", "Kajiado South", "Kajiado West"],
    "Kericho": ["Bureti", "Belgut", "Kipkelion East", "Kipkelion West", "Ainamoi", "Soin/Sigowet"],
    "Bomet": ["Bomet Central", "Bomet East", "Bomet West", "Chepalungu", "Sotik", "Konoin"],
    "Kakamega": ["Lugari", "Likuyani", "Malava", "Lurambi", "Navakholo", "Mumias East", "Mumias West", "Matungu", "Butere", "Khwisero", "Shinyalu", "Ikolomani"],
    "Vihiga": ["Vihiga", "Sabatia", "Hamisi", "Luanda"],
    "Bungoma": ["Mt. Elgon", "Sirisia", "Kabuchai", "Bumula", "Kanduyi", "Webuye East", "Webuye West", "Kimilili", "Tongaren"],
    "Busia": ["Teso North", "Teso South", "Nambale", "Matayos", "Butula", "Funyula", "Budalangi"],
    "Siaya": ["Ugenya", "Ugunja", "Alego Usonga", "Gem", "Bondo", "Rarieda"],
    "Kisumu": ["Kisumu East", "Kisumu West", "Kisumu Central", "Seme", "Nyando", "Muhoroni"],
    "Homa Bay": ["Kasipul", "Kabondo Kasipul", "Karachuonyo", "Rangwe", "Homa Bay Town", "Ndhiwa", "Suba"],
    "Migori": ["Rongo", "Awendo", "Kuria West", "Kuria East", "Nyatike", "Uriri", "Sun East", "Sun West", "Nyaribari Masaba", "Nyaribari Chache"],
    "Kisii": ["Kitutu Chache North", "Kitutu Chache South", "Bobasi", "Bonchari", "South Mugirango", "Bomachoge Borabu"],
    "Nyamira": ["Nyamira North", "Nyamira South", "Borabu", "Manga", "Masaba North", "West Mugirango"],
    "Nairobi": ["Westlands", "Lang'ata", "Kibra", "Kasarani", "Embakasi South", "Embakasi West", "Embakasi Central", "Embakasi North", "Embakasi East", "Makadara", "Kamukunji", "Starehe", "Mathare", "Roysambu", "Ruaraka", "Gatundu South", "Gatundu North"]
};

// Function to update the constituency dropdown based on the selected county
function updateConstituencies() {
    const countySelect = document.getElementById("new_county");
    const constituencySelect = document.getElementById("new_collection_constituency");
    const selectedCounty = countySelect.value;

    // Clear existing options
    constituencySelect.innerHTML = "";

    // Populate options based on selected county
    countyConstituencies[selectedCounty].forEach(constituency => {
        const option = document.createElement("option");
        option.text = constituency;
        option.value = constituency;
        constituencySelect.add(option);
    });
}

// Call the function initially to populate constituencies for the default county
updateConstituencies();

//==================================================================================================================
//PASSWORD VERIFICATION ============================================================================================
//This will be used in all registration forms
//PASSWORD VERIFICATION ============================================================================================
    //PASSWORD VERIFICATION ============================================================================================
    var myInput1 = document.getElementById("myPassword"); // Change variable name to myInput1
    var myInput2 = document.getElementById("myPassword2"); // Variable for the second password field
    var letter = document.getElementById("letter");
    var capital = document.getElementById("capital");
    var number = document.getElementById("number");
    var length = document.getElementById("length");

    // When the user clicks on the password field, show the message box
    myInput1.onfocus = function() {
      document.getElementById("message").style.display = "block";
    }
    myInput2.onfocus = function() { // Adjusted for the second password field
      document.getElementById("message").style.display = "block";
    }

    // When the user clicks outside of the password field, hide the message box
    myInput1.onblur = function() {
      document.getElementById("message").style.display = "block";
    }

    myInput2.onblur = function() { // Adjusted for the second password field
      document.getElementById("message").style.display = "block";
    }

    // When the user starts to type something inside the password field
    myInput1.onkeyup = function() {
      // Validate lowercase letters
      var lowerCaseLetters = /[a-z]/g;
      if(myInput1.value.match(lowerCaseLetters)) { // Change myInput to myInput1
        letter.classList.remove("invalid");
        letter.classList.add("valid");
      } else {
        letter.classList.remove("valid");
        letter.classList.add("invalid");
      }
    }

    myInput2.onkeyup = function() { // Adjusted for the second password field
      // Validate lowercase letters
      var lowerCaseLetters = /[a-z]/g;
      if(myInput2.value.match(lowerCaseLetters)) { // Change myInput to myInput2
        letter.classList.remove("invalid");
        letter.classList.add("valid");
      } else {
        letter.classList.remove("valid");
        letter.classList.add("invalid");
      }
      
      // Validate capital letters, numbers, and length (similar logic as for myInput1)
      var upperCaseLetters = /[A-Z]/g;
      if(myInput2.value.match(upperCaseLetters)) {
        capital.classList.remove("invalid");
        capital.classList.add("valid");
      } else {
        capital.classList.remove("valid");
        capital.classList.add("invalid");
      }

      // Validate numbers
      var numbers = /[0-9]/g;
      if(myInput2.value.match(numbers)) {
        number.classList.remove("invalid");
        number.classList.add("valid");
      } else {
        number.classList.remove("valid");
        number.classList.add("invalid");
      }

      // Validate length
      if(myInput2.value.length >= 8) {
        length.classList.remove("invalid");
        length.classList.add("valid");
      } else {
        length.classList.remove("valid");
        length.classList.add("invalid");
      }
    }

//==================================================================================================================