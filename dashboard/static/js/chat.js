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

    // ------------------ chat contacts? !!!!!!!!!!!! --------------------------------------------------------------------
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

    // --------------- chat window --------------------------
    $("body").on('click', '#chat-contact', function(){
        // alert($(this).attr('contact_id'));
        contact_id = $(this).attr('contact_id');
        $.ajax({url: "/dashboard/chat_view/" + contact_id + '/', 
                dataType: "json",
                success: function(datas){
                                console.log(datas);
                                $('#chat-namebar').text(datas['username']);
                            },
                error: function(xhr, type){alert("'Ajax Error!'");}}
            );
    });
});