/* French initialisation for the jQuery UI date picker plugin. */
/* Written by Keith Wood (kbwood@virginbroadband.com.au) and Stéphane Nahmani (sholby@sholby.net). */
(function($){
	$.datepicker.regional['cs'] = {
		closeText: 'Zavřít',
		prevText: '&#x3c;Předchozí',
		nextText: 'Dal&#x3e;',
		currentText: 'Dnes',
		monthNames: ['Leden','Únor','Březen','Duben','Květen','Červen', 'Červenec','Srpen','Září','Říjen','Listopad','Prosinec'],
		monthNamesShort: ['Led','Úno','Bře','Dub','Kvě','Čvn', 'Čnc','Srp','Zář','Říj','Lis','Pro'],
		dayNames: ['Neděle','Pondělí','Úterý','Středa','Čtvrtek','Pátek','Sobota'],
		dayNamesShort: ['Ne','Po','Út','St','Čt','Pá','So',],
		dayNamesMin: ['Ne','Po','Út','St','Čt','Pá','So',],
		dateFormat: 'dd.mm.yy', firstDay: 1,
		isRTL: false};
	$.datepicker.setDefaults($.datepicker.regional['cs']);
})(grp.jQuery);
