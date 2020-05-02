'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var StudyCard = function (_React$Component) {
  _inherits(StudyCard, _React$Component);

  function StudyCard() {
    var _ref;

    var _temp, _this, _ret;

    _classCallCheck(this, StudyCard);

    for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }

    return _ret = (_temp = (_this = _possibleConstructorReturn(this, (_ref = StudyCard.__proto__ || Object.getPrototypeOf(StudyCard)).call.apply(_ref, [this].concat(args))), _this), _this.state = {
      card_data: []
    }, _temp), _possibleConstructorReturn(_this, _ret);
  }

  _createClass(StudyCard, [{
    key: 'componentDidMount',
    value: function componentDidMount() {
      var _this2 = this;

      var deck_id = window.location.pathname.split('/').pop();
      console.log("PATH :  " + deck_id);
      fetch('http://127.0.0.1:5000/api/study/' + deck_id, { method: 'GET',
        headers: new Headers({ 'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODgwOTY3MjQsIm5iZiI6MTU4ODA5NjcyNCwianRpIjoiMjY4ZjQ2MDAtNzFhZC00ZTY1LThhNjAtZTZjYzM1MmIwYzdhIiwiZXhwIjoxNTg4NzAxNTI0LCJpZGVudGl0eSI6IjVlYTQyMzMyOWM1YWZjNjA4MjBlYzA4MSIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.73vHmWLDkeBVtflBVMKc-FKOY594V8z0nQ8qqsM8OyA' })
      }).then(function (res) {
        return res.json();
      }).then(function (data) {
        _this2.setState({ card_data: data });
        console.log("CARD DATA:  " + card_data);
      }).catch(console.log);
    }
  }, {
    key: 'render',
    value: function render() {
      return React.createElement(
        'div',
        { className: 'row' },
        React.createElement(
          'div',
          { 'class': 'col-xl-6 col-lg-5 mx-auto' },
          React.createElement(
            'div',
            { 'class': 'card shadow mb-4' },
            React.createElement(
              'div',
              { 'class': 'card-header py-3 d-flex flex-row align-items-center justify-content-between' },
              React.createElement(
                'a',
                { href: '#', 'class': 'btn btn-default btn-sm' },
                React.createElement('i', { 'class': 'fa fa-chevron-left' })
              ),
              React.createElement(
                'span',
                { 'class': 'm-0' },
                'Card # -- '
              ),
              React.createElement(
                'div',
                { 'class': 'dropdown no-arrow' },
                React.createElement(
                  'a',
                  { 'class': 'dropdown-toggle', href: '#', role: 'button', id: 'dropdownMenuLink', 'data-toggle': 'dropdown', 'aria-haspopup': 'true', 'aria-expanded': 'false' },
                  React.createElement('i', { 'class': 'fas fa-ellipsis-v fa-sm fa-fw text-gray-400' })
                ),
                React.createElement(
                  'div',
                  { 'class': 'dropdown-menu dropdown-menu-right shadow animated--fade-in', 'aria-labelledby': 'dropdownMenuLink' },
                  React.createElement(
                    'a',
                    { 'class': 'dropdown-item', href: '#' },
                    'Modify Card'
                  ),
                  React.createElement(
                    'a',
                    { 'class': 'dropdown-item', href: '#' },
                    'Skip Card'
                  ),
                  React.createElement('div', { 'class': 'dropdown-divider' }),
                  React.createElement(
                    'a',
                    { 'class': 'dropdown-item', href: '#' },
                    'Something else'
                  )
                )
              )
            ),
            React.createElement(
              'div',
              { 'class': 'card-body text-center' },
              React.createElement(
                'div',
                { 'class': 'row justify-content-center py-3' },
                React.createElement(
                  'div',
                  { 'class': 'col-12 text-center py-3' },
                  this.state.card_data.question
                ),
                React.createElement(
                  'div',
                  { 'class': 'col-6 py-3' },
                  React.createElement('input', { type: 'text form-control-lg', placeholder: 'Your answer...', style: 'width:100%;' })
                )
              ),
              React.createElement(
                'a',
                { id: 'answerButton', href: '#answerArea', 'class': 'btn btn-primary', 'data-toggle': 'collapse', role: 'button',
                  'aria-expanded': 'true', 'aria-controls': 'collapseCardExample', onclick: 'getElementById(\'answerButton\').style.display = \'none\';' },
                'Click to show answer'
              ),
              React.createElement(
                'div',
                { 'class': 'collapse hide', id: 'answerArea' },
                React.createElement(
                  'div',
                  { 'class': 'card-body' },
                  React.createElement('div', null),
                  React.createElement(
                    'div',
                    null,
                    this.state.card_data.answer
                  ),
                  React.createElement('hr', null),
                  React.createElement(
                    'form',
                    { method: 'POST' },
                    React.createElement(
                      'button',
                      _defineProperty({ type: 'submit', name: 'test_result', value: '0', 'class': 'btn btn-danger' }, 'type', 'button'),
                      React.createElement('i', { 'class': 'fas fa-fw fa-times d-md-none' }),
                      React.createElement(
                        'span',
                        { 'class': 'd-none d-sm-inline-block' },
                        'I forgot :('
                      )
                    ),
                    React.createElement(
                      'button',
                      _defineProperty({ type: 'submit', name: 'test_result', value: '1', 'class': 'btn btn-success' }, 'type', 'button'),
                      React.createElement('i', { 'class': 'fas fa-fw fa-check d-md-none' }),
                      React.createElement(
                        'span',
                        { 'class': 'd-none d-sm-inline-block' },
                        'I remember!'
                      )
                    )
                  )
                )
              )
            )
          )
        )
      );
    }
  }]);

  return StudyCard;
}(React.Component);

ReactDOM.render(React.createElement(StudyCard, null), document.querySelector('#card_container'));