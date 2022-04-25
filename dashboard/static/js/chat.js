$(function(){
    $("body").on('click', '.talker_button', function(){
        $('#id_mto').val($(this).attr('talker'));
        $('.talker_button').each(function(){
            $(this).css('background-color', 'white');
        });
        // $(this).css('background-color', 'green');
    });

    $("body").on('click', '#chat_ui', function(){
        $('#chat_li').css('display', 'block');
        $('#chatback').css('display', 'block');
    });

    $("body").on('click', '#x', function(){
        $('#chat_li').css('display', 'none');
        $('#chatback').css('display', 'none');
    });


    // chat UI
    // $('#chat-namebar').click(function(){
    //     $('#chat-box').toggle();
    // });

    $('#chat-icon').click(function(){
        if($('#all-chat').css('display') == 'none')
        {
            $('#chat-contacts').toggle(); 
        }
        else
        {
            $('#chat-contacts').toggle();
            $('#all-chat').toggle();
        }
    });
    $('#chat-contacts').click(function(){
        if($('#all-chat').css('display') == 'none')
        {
            $('#all-chat').toggle();   
        }
        
        
    });

    // ------------------ chat contacts?  --------------------------------------------------------------------
    // 
    // $("body").on('click', '#chat-contact', function(){
    //     // alert($(this).attr('contact_id'));
    //     contact_id = $(this).attr('contact_id');
    //     $.ajax({url: "/dashboard/contact_view/" + contact_id + '/', 
    //             dataType: "json",
    //             success: function(datas){
    //                             console.log(datas);
    //                             $('#chat-namebar').text(datas['username']);
    //                         },
    //             error: function(xhr, type){alert("'Ajax Error!'");}}
    //         );
    // });

    // --------------- chat window --------------------------!!!!!!!!!!!!
    $("body").on('click', '#chat-contact', function(){
        // alert($(this).attr('contact_id'));
        contact_id = $(this).attr('contact_id');
        $.ajax({url: "/dashboard/chat_view/" + contact_id + '/', 
                dataType: "json",
                success: function(datas){
                                console.log(datas);
                                $('#chat-namebar').text(datas['username']);
                                $('#id_mto').val(datas['username']);
                                get_messages(datas);
                            },
                error: function(xhr, type){alert("'Ajax Error!'");}}
            );
    });

    // --------------- grab messages --------------------------!!!!!!!!!!!!
    function get_messages(datas){
        var userContent = $('<div  class="row ps-5 p-2" style="display:block;float:right;width:350px;height:35px;"></div>');
        var contactContent = $('<div class="row p-2" style="display:block;float:right;width:350px;height:35px;"></div>');
        

        $.each(datas['last_msgs'], function(index,item){
            console.log(item);
            userContent.prepend($('<div class="rounded-pill bg-info text-white py-1 px-2" style="float:left;max-width: 150px;">'+item+'</div>'));
            userContent.prepend($('<div class="rounded-pill bg-secondary text-white py-1 px-2" style="float:right;max-width: 150px;">'+item+'</div>'));
            userContent.prepend($('<div class="rounded-pill bg-info text-white py-1 px-2" style="float:left;max-width: 150px;">'+item+'</div>'));
        });
        // $('#tasks').children().remove();
        // console.log(content);
        $('#user-message').append(userContent);
    };

    // --------------- submit messages to db --------------------------!!!!!!!!!!!!
    $("#chat-form").submit(function(e){
        
        e.preventDefault();

        var form = $(this);
        
        // msg = $(this).input('message');
        // console.log("message:"+msg);
        $.ajax({
                type:"POST",
                url: "/dashboard/chat_view/" + contact_id + '/', 
                dataType: "json",
                data: form.serialize(),
                success: function(datas){
                                console.log("!MSG:");
                                // console.log(data);
                                console.log(datas);
                                get_messages(datas);
                                // $('#chat-namebar').text(datas['username']);
                            },
                error: function(xhr, type){alert("'Ajax Error!'");}}
            );
    });
});