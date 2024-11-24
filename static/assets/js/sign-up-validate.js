/* FORM WIZARD VALIDATION SIGN UP ======================================== */

jQuery(function ($) {
    "use strict";

    // Chose here which method to send the email, available:
    // Phpmaimer text/html > phpmailer/registration_phpmailer.php
    // Phpmaimer text/html SMPT > phpmailer/registration_phpmailer_smtp.php
    // PHPmailer with html template > phpmailer/registration_phpmailer_template.php
    // PHPmailer with html template SMTP> phpmailer/registration_phpmailer_template_smtp.php

    $('form#custom').attr('action', 'phpmailer/registration_phpmailer_template.php');

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
            'firstname': 'required',
            'lastname': 'required',
            'email': 'required',
            'telephone': 'required',
            'address': 'required',
            'city': 'required',
            'zip_code': 'required',
            'country': 'required',
            'terms': 'required' // BE CAREFUL: last has no comma
        },
        messages: {
            'firstname': { required: 'Name required' },
            'lastname': { required: 'Last name required' },
            'email': { required: 'Invalid e-mail!' },
            'telephone': { required: 'Telephone required' },
            'address': { required: 'Address required' },
            'city': { required: 'City required' },
            'zip_code': { required: 'Zip code required' },
            'country': { required: 'Country required' },
            'terms': { required: 'Please accept terms' },
        },
        submitHandler: function(form){
            if ($('input#website').val().length == 0) {
                form.submit();
            }
        }
    });

});
			