/* FORM WIZARD RESERVATION SIGN UP ======================================== */

jQuery(function ($) {
    "use strict";

    // Chose here which method to send the email, available:
    // Simple phpmail text/plain > reservation_send.php (default)
    // Phpmaimer text/html > phpmailer/reservation_phpmailer.php
    // Phpmaimer text/html SMPT > phpmailer/reservation_phpmailer_smtp.php
    // PHPmailer with html template > phpmailer/reservation_phpmailer_template.php
    // PHPmailer with html template SMTP> phpmailer/reservation_phpmailer_template_smtp.php

    $('form#custom').attr('action', 'phpmailer/reservation_phpmailer_template.php');

    $('#custom').stepy({
        backLabel: 'Previous',
        block: true,
        errorImage: false,
        nextLabel: 'Next',
        titleClick: true,
        description: true,
        legend: false,
        validate: true
    });


    $('#custom').validate({

        errorPlacement: function(error, element) {

            $('#custom .stepy-error').append(error);
        },
        rules: {
            'check_in': 'required',
            'adults': 'required',
            'room_type': 'required',
            'firstname': 'required',
            'lastname': 'required',
            'email': 'required',
            'telephone': 'required',
            'terms': 'required' // BE CAREFUL: last has no comma
        },
        messages: {
            'check_in': { required: 'Check in required' },
            'adults': { required: 'Adults required' },
            'room_type': { required: 'Room type required' },
            'firstname': { required: 'Name required' },
            'lastname': { required: 'Last name required' },
            'email': { required: 'Invalid e-mail!' },
            'telephone': { required: 'Telephone required' },
            'terms': { required: 'Please accept terms' },
        },
        submitHandler: function(form){
            if ($('input#website').val().length == 0) {
                form.submit();
            }
        }
    });

});
			