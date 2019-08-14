/**
 * @license Copyright (c) 2003-2019, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

/**
 * @license Copyright (c) 2003-2019, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function( config ) {
	config.language = 'zh-cn';
//	config.uiColor = '#F7B42C';
	config.height = 775;
	config.toolbarCanCollapse = false; //禁用折叠工具栏
	config.codeSnippet_theme = 'default';
	config.tabSpaces = 4;
	config.toolbar = [
		{ name: 'styles', items: [  '-', 'Styles', 'Format', 'Font', 'FontSize' ] },
		{ name: 'basicstyles', items: [ 'Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', 'TextColor', 'BGColor' ] },
		{ name: 'paragraph', items: [ 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', 'Outdent', 'Indent', 'NumberedList', 'BulletedList', '-' ] },
		{ name: 'clipboard', items: [ 'Paste', 'PasteText', 'PasteFromWord' ] },
		{ name: 'links', items: [ 'Link', 'Unlink', 'Anchor', 'CodeSnippet', 'EasyImageUpload', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'Blockquote', 'Iframe',  '-'] },
		{ name: 'document', items: [ 'Undo', 'Redo', 'Maximize', 'Preview', 'Source', 'About' ] }
	];
	config.image_previewText = ' ';
	config.filebrowserImageUploadUrl= "/blog/uploadEditorImage/"; //图片上传地址
    config.uploadFileRootUrl=uploadImageRootLoaction;
};






/*

CKEDITOR.editorConfig = function( config ) {
	config.toolbarGroups = [
		{ name: 'document', groups: [ 'mode', 'document', 'doctools' ] },
		{ name: 'clipboard', groups: [ 'clipboard', 'undo' ] },
		{ name: 'editing', groups: [ 'find', 'selection', 'spellchecker', 'editing' ] },
		{ name: 'forms', groups: [ 'forms' ] },
		'/',
		{ name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
		{ name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi', 'paragraph' ] },
		{ name: 'links', groups: [ 'links' ] },
		{ name: 'insert', groups: [ 'insert' ] },
		'/',
		{ name: 'styles', groups: [ 'styles' ] },
		{ name: 'colors', groups: [ 'colors' ] },
		{ name: 'tools', groups: [ 'tools' ] },
		{ name: 'others', groups: [ 'others' ] },
		{ name: 'about', groups: [ 'about' ] }
	];
};

*/
