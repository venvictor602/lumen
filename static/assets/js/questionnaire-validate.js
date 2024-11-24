/* FORM WIZARD RESERVATION SIGN UP ======================================== */

jQuery(function ($) {
    "use strict";

    // Chose here which method to send the email, available:
    // Phpmaimer text/html > phpmailer/questionnaire_phpmailer.php
    // Phpmaimer text/html SMPT > phpmailer/questionnairephpmailer_smtp.php
    // PHPmailer with html template > phpmailer/questionnaire_phpmailer_template.php
    // PHPmailer with html template SMTP> phpmailer/questionnaire_phpmailer_template_smtp.php

    $('form#custom').attr('action', 'phpmailer/questionnaire_phpmailer_template.php');

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
            'satisfaction': 'required',
            'question_2[]': 'required',
            'firstname': 'required',
            'lastname': 'required',
            'email': 'required',
            'telephone': 'required',
            'terms': 'required' // BE CAREFUL: last has no comma
        },
        messages: {
            'satisfaction': { required: 'Answer required' },
            'question_2[]': { required: 'Answer required' },
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
			