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
    $('#chat-namebar').click(function(){
        $('#chat-box').toggle();
    });

    $('#chat-icon').click(function(){
        if($('#chat-box').css('display') == 'none' && $('#chat-namebar').css('display') == 'none')
        {
            $('#chat-box').toggle();
            $('#chat-namebar').toggle();
            $('#chat-contacts').toggle();
        }
        else if($('#chat-box').css('display') == 'none')
        {
            $('#chat-namebar').toggle();
            $('#chat-contacts').toggle();
        }
        else
        {
            $('#chat-box').toggle();
            $('#chat-namebar').toggle();
            $('#chat-contacts').toggle();
        }
        
    });

});