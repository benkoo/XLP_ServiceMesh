/*!
 * @copyright See AUTHORS.txt
 * @license GPL-2.0-or-later
 */
( function ( $, mw ) {
	'use strict';
	mw.cx.widgets = mw.cx.widgets || {};

	mw.cx.widgets.spinner = function () {
		return $( '<div>' )
			.addClass( 'cx-spinner' )
			.append(
				$( '<div>' ).addClass( 'bounce1' ),
				$( '<div>' ).addClass( 'bounce2' ),
				$( '<div>' ).addClass( 'bounce3' )
			);
	};
}( jQuery, mediaWiki ) );
