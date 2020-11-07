jQuery(function() {
    emotions = [
        "happy",
        "hopeful",
        "adventure",
        "chill",
        "dreamy",
        "sad"
    ]
    $('#edit_moods').on("click", function(){
        $("#done_moods").removeAttr("hidden")
        for(i = 0; i < 6; i++) {
            $(`#cm${emotions[i]}`).removeAttr("hidden")
            $(`#cp${emotions[i]}`).removeAttr("hidden")
            $(`#gm${emotions[i]}`).removeAttr("hidden")
            $(`#gp${emotions[i]}`).removeAttr("hidden")

            
        }
    })
    dict_current = {
        "happy" : 0,
        "hopeful" : 0, 
        "adventure" : 0,
        "chill" : 0,
        "dreamy" : 0,
        "sad" : 0,
    }
    dict_goal = {
        "happy" : 0,
        "hopeful" : 0, 
        "adventure" : 0,
        "chill" : 0,
        "dreamy" : 0,
        "sad" : 0,
    }
    for(i = 0; i < 6; i++) {
        $(`#cm${emotions[i]}`).on("click", function() {
            $(`#c${$(this).attr("bar")}`).css({
                'width' : $(`#c${$(this).attr("bar")}`).width()  * 0.8
            });
            dict_current[`${$(this).attr("bar")}`] -= 1;
        })
        $(`#cp${emotions[i]}`).on("click", function() {
            $(`#c${$(this).attr("bar")}`).css({
                'width' : $(`#c${$(this).attr("bar")}`).width()  * 1.2
            });
            dict_current[`${$(this).attr("bar")}`] += 1;
            
        })
        $(`#gm${emotions[i]}`).on("click", function() {
            $(`#g${$(this).attr("bar")}`).css({
                'width' : $(`#g${$(this).attr("bar")}`).width()  * 0.8
            });
            console.log(`#g${$(this).attr("bar")}`)
            dict_goal[`${$(this).attr("bar")}`] -= 1;

        })
        $(`#gp${emotions[i]}`).on("click", function() {

            $(`#g${$(this).attr("bar")}`).css({
                'width' : $(`#g${$(this).attr("bar")}`).width()  * 1.2
            });

            dict_goal[`${$(this).attr("bar")}`] += 1;
            
        })
   
    }

    $('#done_moods').on("click", function() {
        $("#done_moods").attr("hidden", true);
        for(i = 0; i < 6; i++) {
            $(`#cm${emotions[i]}`).attr("hidden", true)
            $(`#cp${emotions[i]}`).attr("hidden", true)
            $(`#gm${emotions[i]}`).attr("hidden", true)
            $(`#gp${emotions[i]}`).attr("hidden", true)
            
        }

        dict = {
            "current"  : dict_current,
            "goal" : dict_goal
        }
        
       
        const csrftoken = Cookies.get('csrftoken');
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
          });
           $.ajax({
              type: 'POST',
              url: $('#done_moods').attr("action"),
              data: dict,
              name: 'new_data'
          }).done(function(data) {
              if(data["status"] == "fail") {
                console.log("here");
                $("#error").show();
                $("#error").text("Invalid credentials");
              } else {
                window.location.reload()
              }
          });
        

    })
    

    // $.ajax({
    //     method: 'POST',
    //     url: $('#login_form').attr("action"),
        
    // }).done(function(data) {
    //     console.log(`Successful request. Fetched data ${data}`);
    // }).fail(function(jqXHR, textStatus) {
    //     alert(`Request failed: ${textStatus}`);
    // });
})