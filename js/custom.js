function isEmail(email) {
  var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  return regex.test(email);
}
function getURLParameter(name) {
    return decodeURI(
        (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,null])[1]
    );
}

$(function() {
	if (window.location.pathname == '/') {
		onResize();
		$(window).bind('resize', onResize);
	};
	$('#email-signup-container button').click(function(e) {
		e.preventDefault();
		if (isEmail($('#email-signup').val())) {
			$('form').submit();
			alert('Thank you.');
		} else {
			alert('Please enter a valid email address.');
		}
	});
});

function onResize() {
	var signup = $('#sign-up');
	var footer = $('footer');
	if((footer.position().top - (signup.position().top + signup.height())) < 300) {
		$('#phone-image').css('display','none');
	} else {
		$('#phone-image').css('display','block');
	}
};
/*$(function() {
	if (window.location.pathname == '/survey1') {
		$('.help-inline').hide();
		commentsText1();
	}
	else if (window.location.pathname == '/survey2') {
		$( "#currentAmountSlider" ).slider({
			value:65,
			min: 0,
			max: 250,
			step: 5,
			slide: function( event, ui ) {
				$( "#currentAmount" ).val( ui.value );
			}
		});
		$( "#currentAmount" ).val( $( "#currentAmountSlider" ).slider( "value" ) );

		$( "#amountMinutesSlider" ).slider({
			value:1000,
			min: 0,
			max: 3000,
			step: 50,
			slide: function( event, ui ) {
				$( "#amountMinutes" ).val( ui.value );
			}
		});
		$( "#amountMinutes" ).val( $( "#amountMinutesSlider" ).slider( "value" ) );

		$( "#amountTextsSlider" ).slider({
			value:1000,
			min: 0,
			max: 3000,
			step: 50,
			slide: function( event, ui ) {
				$( "#amountTexts" ).val( ui.value );
			}
		});
		$( "#amountTexts" ).val( $( "#amountTextsSlider" ).slider( "value" ) );

		$( "#amountDataSlider" ).slider({
			value:1000,
			min: 0,
			max: 15000,
			step: 50,
			slide: function( event, ui ) {
				$( "#amountData" ).val( ui.value );
			}
		});
		$( "#amountData" ).val( $( "#amountDataSlider" ).slider( "value" ) );

		$('.help-inline').hide();
		currentCarrier2();
	}
	$('.tabbable .tab-pane a').unbind();
});
function validate_zip(zip) {
	var reg = /^([0-9][0-9][0-9][0-9][0-9])?$/;
	return reg.test(zip);
}
function isEmail(email) {
  var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  return regex.test(email);
}


function sameCarrier1() {
	$('fieldset').hide();
	$('#same-carrier').show();
	$('#next-button').show();
	$('#back-button').hide();
	$('#next-button').click(function() {
		$('#back-button').unbind();
		$('#next-button').unbind();
		badCarrier1();
	});
}
function badCarrier1() {
	$('fieldset').hide();
	$('#bad-carrier').show();
	$('#next-button').show();
	$('#back-button').show();
	$('#next-button').click(function() {
		$('#back-button').unbind();
		$('#next-button').unbind();
		preferredDevice1();
	});
	$('#back-button').click(function() {
		$('#back-button').unbind();
		$('#next-button').unbind();
		sameCarrier1();
	});
}
function preferredDevice1() {
	$('fieldset').hide();
	$('#preferred-device').show();
	$('#next-button').show();
	$('#back-button').show();
	$('#next-button').click(function() {
		$('#back-button').unbind();
		$('#next-button').unbind();
		zipcode1();
	});
	$('#back-button').click(function() {
		$('#back-button').unbind();
		$('#next-button').unbind();
		badCarrier1();
	});
}
function zipcode1() {
	$('fieldset').hide();
	$('#zipcode').show();
	$('#next-button').show();
	$('#back-button').show();
	if ($('#zipcode input:checkbox').is(':checked')) {
		$('#workZipcode').hide();
		$('#work-zipcode .help-inline').hide();
	} else {
		$('#workZipcode').show();
		if ($('#work-zipcode').hasClass('error')) {
			$('#work-zipcode .help-inline').show();
		}
	}
	$('#next-button').click(function() {
		var home = validate_zip($('#homeZipcode').val());
		var work = validate_zip($('#workZipcode').val());
		if (!home) {
			$('#home-zipcode').addClass('error');
			$('#home-zipcode .help-inline').show();
		} else {
			$('#home-zipcode').removeClass('error');
			$('#home-zipcode .help-inline').hide();
		}
		if (!work && !$('#zipcode input:checkbox').is(':checked')) {
			$('#work-zipcode').addClass('error');
			$('#work-zipcode .help-inline').show();
		} else {
			$('#work-zipcode').removeClass('error');
			$('#work-zipcode .help-inline').hide();
		}
		if (home && (work || $('#zipcode input:checkbox').is(':checked'))) {
			$('#back-button').unbind();
			$('#next-button').unbind();
			travel1();
		}
	});
	$('#back-button').click(function() {
		$('#back-button').unbind();
		$('#next-button').unbind();
		preferredDevice1();
	});
	$('#zipcode input:checkbox').click(function() {
		if ($(this).is(':checked')) {
			$('#workZipcode').hide("slow");
			$('#work-zipcode .help-inline').hide("slow");
		} else {
			$('#workZipcode').show("slow");
			if ($('#work-zipcode').hasClass('error')) {
				$('#work-zipcode .help-inline').show('slow');
			}
		}
	})
}
function travel1() {
	$('fieldset').hide();
	$('#travel').show();
	$('#next-button').show();
	$('#back-button').show();
	if ($('input[name="travel"]:checked').val() == 'yes') {
		$('#travel-zip').show();
	} else {
		$('#travel-zip').hide();
	}
	$('#next-button').click(function() {
		var zip1 = validate_zip($('#travelZipcode1').val());
		var zip2 = validate_zip($('#travelZipcode2').val());
		var zip3 = validate_zip($('#travelZipcode3').val());
		var zip4 = validate_zip($('#travelZipcode4').val());
		var zip5 = validate_zip($('#travelZipcode5').val());
		if (zip1) {
			$('#travelZip1').removeClass('error');
			$('#travelZip1 .help-inline').hide();
		} else {
			$('#travelZip1').addClass('error');
			$('#travelZip1 .help-inline').show();
		}
		if (zip2) {
			$('#travelZip2').removeClass('error');
			$('#travelZip2 .help-inline').hide();
		} else {
			$('#travelZip2').addClass('error');
			$('#travelZip2 .help-inline').show();
		}
		if (zip3) {
			$('#travelZip3').removeClass('error');
			$('#travelZip3 .help-inline').hide();
		} else {
			$('#travelZip3').addClass('error');
			$('#travelZip3 .help-inline').show();
		}
		if (zip4) {
			$('#travelZip4').removeClass('error');
			$('#travelZip4 .help-inline').hide();
		} else {
			$('#travelZip4').addClass('error');
			$('#travelZip4 .help-inline').show();
		}
		if (zip5) {
			$('#travelZip5').removeClass('error');
			$('#travelZip5 .help-inline').hide();
		} else {
			$('#travelZip5').addClass('error');
			$('#travelZip5 .help-inline').show();
		}
		if (zip1 && zip2 && zip3 && zip4 && zip5) {
			$('#back-button').unbind();
			$('#next-button').unbind();
			commentsText1();
		}
	});
	$('#back-button').click(function() {
		$('#back-button').unbind();
		$('#next-button').unbind();
		zipcode1();
	});
	$('#travel .radio input').change(function() {
		if ($('input[name="travel"]:checked').val() == 'yes') {
			$('#travel-zip').show('slow');
		} else {
			$('#travel-zip').hide('slow');
		}
	})
}
function commentsText1() {
	$('fieldset').hide();
	$('#comments-text').show();
	$('#next-button').show();
	$('#next-button').html('Next &raquo;');
	$('#back-button').hide();
	$('#next-button').click(function() {

		$('#back-button').unbind();
		$('#next-button').unbind();
		personalInfo1();
	});
	$('#back-button').click(function() {
		$('#back-button').unbind();
		$('#next-button').unbind();
		travel1();
	});
}
function personalInfo1() {
	$('fieldset').hide();
	$('#personal-info').show();
	$('#next-button').show();
	$('#next-button').html('Finish');
	$('#back-button').show();
	$('#next-button').click(function() {
		if (isEmail($('#personal-info #emailField').val())) {
			$('#personal-info .control-group').removeClass('error');
			$('#personal-info .help-inline').hide();
			$('form').submit();
			$('#back-button').unbind();
			$('#next-button').unbind();
		} else {
			$('#personal-info .control-group').addClass('error');
			$('#personal-info .help-inline').show();
		}
	});
	$('#back-button').click(function() {
		$('#back-button').unbind();
		$('#next-button').unbind();
		commentsText1();
	});
}


function currentCarrier2() {
	$('fieldset').hide();
	$('#current-carrier').show();
	$('#next-button').show();
	$('#back-button').hide();
	$('#next-button').click(function() {
		$('#next-button').unbind();
		currentAmount2();
	});	
}
function currentAmount2() {
	$('fieldset').hide();
	$('#current-amount').show();
	$('#next-button').show();
	$('#back-button').show();

	$('#next-button').click(function() {
		if ($.isNumeric($('#currentAmount').val()) && parseFloat($('#currentAmount').val()) >= 0.0) {
			$('#current-amount .control-group').removeClass('error');
			$('#current-amount .help-inline').hide();
			$('#back-button').unbind();
			$('#next-button').unbind();
			//sameCarrier2();
			amountMinutes2();
		} else {
			$('#current-amount .control-group').addClass('error');
			$('#current-amount .help-inline').show();
		}
	});
	$('#back-button').click(function() {
		$('#back-button').unbind();
		$('#next-button').unbind();
		currentCarrier2();
	});
}
function sameCarrier2() {
	$('fieldset').hide();
	$('#same-carrier').show();
	$('#next-button').show();
	$('#back-button').show();
	$('#next-button').click(function() {
		$('#back-button').unbind();
		$('#next-button').unbind();
		badCarrier2();
	});
	$('#back-button').click(function() {
		$('#back-button').unbind();
		$('#next-button').unbind();
		currentAmount2();
	});
}
function badCarrier2() {
	$('fieldset').hide();
	$('#bad-carrier').show();
	$('#next-button').show();
	$('#back-button').show();
	$('#next-button').click(function() {
		$('#back-button').unbind();
		$('#next-button').unbind();
		preferredDevice2();
	});
	$('#back-button').click(function() {
		$('#back-button').unbind();
		$('#next-button').unbind();
		sameCarrier2();
	});
}
function preferredDevice2() {
	$('fieldset').hide();
	$('#preferred-device').show();
	$('#next-button').show();
	$('#back-button').show();
	$('#next-button').click(function() {
		$('#back-button').unbind();
		$('#next-button').unbind();
		zipcode2();
	});
	$('#back-button').click(function() {
		$('#back-button').unbind();
		$('#next-button').unbind();
		badCarrier2();
	});
}
function zipcode2() {
	$('fieldset').hide();
	$('#zipcode').show();
	$('#next-button').show();
	$('#back-button').show();
	if ($('#zipcode input:checkbox').is(':checked')) {
		$('#workZipcode').hide();
		$('#work-zipcode .help-inline').hide();
	} else {
		$('#workZipcode').show();
		if ($('#work-zipcode').hasClass('error')) {
			$('#work-zipcode .help-inline').show();
		}
	}
	$('#next-button').click(function() {
		var home = validate_zip($('#homeZipcode').val());
		var work = validate_zip($('#workZipcode').val());
		if (!home) {
			$('#home-zipcode').addClass('error');
			$('#home-zipcode .help-inline').show();
		} else {
			$('#home-zipcode').removeClass('error');
			$('#home-zipcode .help-inline').hide();
		}
		if (!work && !$('#zipcode input:checkbox').is(':checked')) {
			$('#work-zipcode').addClass('error');
			$('#work-zipcode .help-inline').show();
		} else {
			$('#work-zipcode').removeClass('error');
			$('#work-zipcode .help-inline').hide();
		}
		if (home && (work || $('#zipcode input:checkbox').is(':checked'))) {
			$('#back-button').unbind();
			$('#next-button').unbind();
			travel2();
		}
	});
	$('#back-button').click(function() {
		$('#back-button').unbind();
		$('#next-button').unbind();
		preferredDevice2();
	});
	$('#zipcode input:checkbox').click(function() {
		if ($(this).is(':checked')) {
			$('#workZipcode').hide("slow");
			$('#work-zipcode .help-inline').hide("slow");
		} else {
			$('#workZipcode').show("slow");
			if ($('#work-zipcode').hasClass('error')) {
				$('#work-zipcode .help-inline').show('slow');
			}
		}
	})
}
function travel2() {
	$('fieldset').hide();
	$('#travel').show();
	$('#next-button').show();
	$('#back-button').show();
	if ($('input[name="travel"]:checked').val() == 'yes') {
		$('#travel-zip').show();
	} else {
		$('#travel-zip').hide();
	}
	$('#next-button').click(function() {
		var zip1 = validate_zip($('#travelZipcode1').val());
		var zip2 = validate_zip($('#travelZipcode2').val());
		var zip3 = validate_zip($('#travelZipcode3').val());
		var zip4 = validate_zip($('#travelZipcode4').val());
		var zip5 = validate_zip($('#travelZipcode5').val());
		if (zip1) {
			$('#travelZip1').removeClass('error');
			$('#travelZip1 .help-inline').hide();
		} else {
			$('#travelZip1').addClass('error');
			$('#travelZip1 .help-inline').show();
		}
		if (zip2) {
			$('#travelZip2').removeClass('error');
			$('#travelZip2 .help-inline').hide();
		} else {
			$('#travelZip2').addClass('error');
			$('#travelZip2 .help-inline').show();
		}
		if (zip3) {
			$('#travelZip3').removeClass('error');
			$('#travelZip3 .help-inline').hide();
		} else {
			$('#travelZip3').addClass('error');
			$('#travelZip3 .help-inline').show();
		}
		if (zip4) {
			$('#travelZip4').removeClass('error');
			$('#travelZip4 .help-inline').hide();
		} else {
			$('#travelZip4').addClass('error');
			$('#travelZip4 .help-inline').show();
		}
		if (zip5) {
			$('#travelZip5').removeClass('error');
			$('#travelZip5 .help-inline').hide();
		} else {
			$('#travelZip5').addClass('error');
			$('#travelZip5 .help-inline').show();
		}
		if (zip1 && zip2 && zip3 && zip4 && zip5) {
			$('#back-button').unbind();
			$('#next-button').unbind();
			amountMinutes2();
		}
	});
	$('#back-button').click(function() {
		$('#back-button').unbind();
		$('#next-button').unbind();
		zipcode2();
	});
	$('#travel .radio input').change(function() {
		if ($('input[name="travel"]:checked').val() == 'yes') {
			$('#travel-zip').show('slow');
		} else {
			$('#travel-zip').hide('slow');
		}
	})
}
function amountMinutes2() {
	$('fieldset').hide();
	$('#amount-minutes').show();
	$('#next-button').show();
	$('#back-button').show();

	$('#next-button').click(function() {
		if ($.isNumeric($('#amountMinutes').val()) && parseFloat($('#amountMinutes').val()) >= 0.0) {
			$('#amount-minutes .control-group').removeClass('error');
			$('#amount-minutes .help-inline').hide();
			$('#back-button').unbind();
			$('#next-button').unbind();
			amountTexts2();
		} else {
			$('#amount-minutes .control-group').addClass('error');
			$('#amount-minutes .help-inline').show();
		}
	});
	$('#back-button').click(function() {
		$('#back-button').unbind();
		$('#next-button').unbind();
		//travel2();
		currentAmount2();
	});
}
function amountTexts2() {
	$('fieldset').hide();
	$('#amount-texts').show();
	$('#next-button').show();
	$('#back-button').show();

	$('#next-button').click(function() {
		if ($.isNumeric($('#amountTexts').val()) && parseFloat($('#amountTexts').val()) >= 0.0) {
			$('#amount-texts .control-group').removeClass('error');
			$('#amount-texts .help-inline').hide();
			$('#back-button').unbind();
			$('#next-button').unbind();
			amountData2();
		} else {
			$('#amount-texts .control-group').addClass('error');
			$('#amount-texts .help-inline').show();
		}
	});
	$('#back-button').click(function() {
		$('#back-button').unbind();
		$('#next-button').unbind();
		amountMinutes2();
	});
}
function amountData2() {
	$('fieldset').hide();
	$('#amount-data').show();
	$('#next-button').show();
	$('#back-button').show();

	$('#next-button').click(function() {
		if ($.isNumeric($('#amountData').val()) && parseFloat($('#amountData').val()) >= 0.0) {
			$('#amount-data .control-group').removeClass('error');
			$('#amount-data .help-inline').hide();
			$('#back-button').unbind();
			$('#next-button').unbind();
			commentsText2();
		} else {
			$('#amount-data .control-group').addClass('error');
			$('#amount-data .help-inline').show();
		}
	});
	$('#back-button').click(function() {
		$('#back-button').unbind();
		$('#next-button').unbind();
		amountTexts2();
	});
}
function commentsText2() {
	$('fieldset').hide();
	$('#comments-text').show();
	$('#next-button').show();
	$('#next-button').html('Next &raquo;');
	$('#back-button').show();
	$('#next-button').click(function() {

		$('#back-button').unbind();
		$('#next-button').unbind();
		personalInfo2();
	});
	$('#back-button').click(function() {
		$('#back-button').unbind();
		$('#next-button').unbind();
		amountData2();
	});
}
function personalInfo2() {
	$('fieldset').hide();
	$('#personal-info').show();
	$('#next-button').show();
	$('#next-button').html('Finish');
	$('#back-button').show();
	$('#next-button').click(function() {
		if (isEmail($('#personal-info #emailField').val())) {
			$('#personal-info .control-group').removeClass('error');
			$('#personal-info .help-inline').hide();
			$('form').submit();
			$('#back-button').unbind();
			$('#next-button').unbind();
		} else {
			$('#personal-info .control-group').addClass('error');
			$('#personal-info .help-inline').show();
		}
	});
	$('#back-button').click(function() {
		$('#back-button').unbind();
		$('#next-button').unbind();
		commentsText2();
	});
}
*/