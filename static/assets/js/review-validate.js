/* FORM WIZARD REVIEW SIGN UP ======================================== */

jQuery(function ($) {
    "use strict";

    // Chose here which method to send the email, available:
    // Phpmaimer text/html > phpmailer/review_phpmailer.php
    // Phpmaimer text/html SMPT > phpmailer/review_phpmailer_smtp.php
    // PHPmailer with html template > phpmailer/review_phpmailer_template.php
    // PHPmailer with html template SMTP> phpmailer/review_phpmailer_template_smtp.php

    $('form#custom').attr('action', 'phpmailer/review_phpmailer_template.php');

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
            'rating_input_1': 'required',
            'rating_input_2': 'required',
            'rating_input_3': 'required',
            'rating_input_4': 'required',
            'review': 'required',
            'firstname': 'required',
            'lastname': 'required',
            'email': 'required',
            'terms': 'required' // BE CAREFUL: last has no comma
        },
        messages: {
            'rating_input_1': { required: 'Rate Service' },
            'rating_input_2': { required: 'Rate Product' },
            'rating_input_3': { required: 'Rate Support' },
            'rating_input_4': { required: 'Rate satisfaction' },
            'review': { required: 'Review required' },
            'firstname': { required: 'Name required' },
            'lastname': { required: 'Last name required' },
            'email': { required: 'Email required' },
            'terms': { required: 'Please accept terms' },
        },
        submitHandler: function(form){
            if ($('input#website').val().length == 0) {
                form.submit();
            }
        }
    });

});
			