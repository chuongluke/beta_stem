/*function uploadAttachment(this){
	var inputfile = $('input[name="attachment"]');
	var target = inputfile.target;
    if (target.val() !== '') {

        var filename = target.val().replace(/.*[\\\/]/,'');

        // submit file
        $(this).parent().each(target[0].files, function(file){
            var querydata = new FormData();
            querydata.append('callback', 'oe_fileupload_temp2');
            querydata.append('ufile',file);
            querydata.append('model', 'res.partner');
            querydata.append('id', '0');
            $.ajax({
                url: '/web/binary/upload_attachment',
                type: 'POST',
                data: querydata,
                cache: false,
                processData: false,  
                contentType: false,
                success: function(result){
                    console.log('-------------success------------');
                },
                error: function(result){
                    console.log('---------------error--------------');
                },
            });

        });
    }
}*/