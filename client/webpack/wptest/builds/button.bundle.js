webpackJsonp([1],{

/***/ 16:
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__(1)(undefined);
// imports


// module
exports.push([module.i, ".button {\n  background: tomato;\n  color: white; }\n", ""]);

// exports


/***/ }),

/***/ 18:
/***/ (function(module, exports) {

module.exports = "<a class=\"button\" href=\"{{link}}\">{{text}}</a>\n";

/***/ }),

/***/ 20:
/***/ (function(module, exports, __webpack_require__) {

// style-loader: Adds some css to the DOM by adding a <style> tag

// load the styles
var content = __webpack_require__(16);
if(typeof content === 'string') content = [[module.i, content, '']];
// add the styles to the DOM
var update = __webpack_require__(2)(content, {});
if(content.locals) module.exports = content.locals;
// Hot Module Replacement
if(false) {
	// When the styles change, update the <style> tags
	if(!content.locals) {
		module.hot.accept("!!../../node_modules/css-loader/index.js!../../node_modules/sass-loader/lib/loader.js!./Button.scss", function() {
			var newContent = require("!!../../node_modules/css-loader/index.js!../../node_modules/sass-loader/lib/loader.js!./Button.scss");
			if(typeof newContent === 'string') newContent = [[module.id, newContent, '']];
			update(newContent);
		});
	}
	// When the module is disposed, remove the <style> tags
	module.hot.dispose(function() { update(); });
}

/***/ }),

/***/ 3:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _jquery = __webpack_require__(14);

var _jquery2 = _interopRequireDefault(_jquery);

var _Button = __webpack_require__(18);

var _Button2 = _interopRequireDefault(_Button);

var _mustache = __webpack_require__(15);

var _mustache2 = _interopRequireDefault(_mustache);

__webpack_require__(20);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var Button = function () {
    function Button(link) {
        _classCallCheck(this, Button);

        this.link = link;
    }

    _createClass(Button, [{
        key: 'onClick',
        value: function onClick(event) {
            event.preventDefault();
            alert(this.link);
        }
    }, {
        key: 'render',
        value: function render(node) {
            var text = (0, _jquery2.default)(node).text();
            // ボタンの描画
            (0, _jquery2.default)(node).html(_mustache2.default.render(_Button2.default, { text: text }));
            // リスナーを割り当て
            (0, _jquery2.default)('.button').click(this.onClick.bind(this));
        }
    }]);

    return Button;
}();

exports.default = Button;

/***/ })

});