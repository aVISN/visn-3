$(function(){
    function create_content(datas){
        var content = $('<ul class="ps-0"></ul>');
        $.each(datas['task_texts'], function(index, item){
            content.append($('<li class="mb-2 btn btn-lg btn-block btn-warning" style="width:100%; list-style-type:none;background-color: bisque;">' + item + '</li>'));
        });
        $('#tasks').children().remove();
        $('#tasks').append(content);
    };
    function create_content2(datas){
        var content = $('<ul class="ps-0"></ul>');
        $.each(datas['file_infos'], function(index, item){
            content.append($('<li class="mb-2 btn btn-lg btn-block btn-success text-black" style="width:100%;list-style-type:none;background-color: aquamarine;">' + item + '</li>'));
        });
        $('#updates').children().remove();
        $('#updates').append(content);
    };

    $("body").on('click', '#proj_disp .row .col', function(){
        // alert($(this).attr('project_id'));
        project_id = $(this).attr('project_id');
        $.ajax({url: "/dashboard/project_view/" + project_id + '/', 
                dataType: "json",
                success: function(datas){
                                var deadlineconvert = new Date(datas['deadline']);
                                console.log(datas);
                                $('.project_name').text(datas['name']);
                                $('.project_deadline').text(deadlineconvert);
                                $('.project_discription').text(datas['discription']);
                                $('.file_number').text(datas['file_number']);
                                $('.create_user').text(datas['create_user']);
                                create_content(datas);
                                create_content2(datas);
                            },
                error: function(xhr, type){alert("'Ajax Error!'");}}
            );
    });

    $('#proj_disp .row .col').eq(0).trigger('click');

    // $("body").on('click', '#chat_ui', function(){
    //     $('#chat_li').css('display', 'block');
    //     $('#chatback').css('display', 'block');
    // });

    // $("body").on('click', '#x', function(){
    //     $('#chat_li').css('display', 'none');
    //     $('#chatback').css('display', 'none');
    // });

});