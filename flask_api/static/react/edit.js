'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var CardsContainer = function (_React$Component) {
  _inherits(CardsContainer, _React$Component);

  function CardsContainer() {
    var _ref;

    var _temp, _this, _ret;

    _classCallCheck(this, CardsContainer);

    for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }

    return _ret = (_temp = (_this = _possibleConstructorReturn(this, (_ref = CardsContainer.__proto__ || Object.getPrototypeOf(CardsContainer)).call.apply(_ref, [this].concat(args))), _this), _this.state = {
      cards_data: [],
      deck_id: 0
    }, _temp), _possibleConstructorReturn(_this, _ret);
  }

  _createClass(CardsContainer, [{
    key: 'componentDidMount',
    value: function componentDidMount() {
      var _this2 = this;

      this.state.deck_id = window.location.pathname.split('/').pop();
      fetch('http://127.0.0.1:5000/api/decks/' + this.state.deck_id + "/cards", { method: 'GET',
        headers: new Headers({ 'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODgwOTY3MjQsIm5iZiI6MTU4ODA5NjcyNCwianRpIjoiMjY4ZjQ2MDAtNzFhZC00ZTY1LThhNjAtZTZjYzM1MmIwYzdhIiwiZXhwIjoxNTg4NzAxNTI0LCJpZGVudGl0eSI6IjVlYTQyMzMyOWM1YWZjNjA4MjBlYzA4MSIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.73vHmWLDkeBVtflBVMKc-FKOY594V8z0nQ8qqsM8OyA' })
      }).then(function (res) {
        return res.json();
      }).then(function (data) {
        _this2.setState({ cards_data: data });
      }).catch(console.log);
    }
  }, {
    key: 'render',
    value: function render() {
      var cards = [];
      this.state.cards_data.forEach(function (card) {
        cards.push(React.createElement(CardBox, { card: card }));
      });
      return React.createElement(
        'div',
        { className: 'row' },
        cards
      );
    }
  }]);

  return CardsContainer;
}(React.Component);

var ListBox = function (_React$Component2) {
  _inherits(ListBox, _React$Component2);

  function ListBox(props) {
    _classCallCheck(this, ListBox);

    return _possibleConstructorReturn(this, (ListBox.__proto__ || Object.getPrototypeOf(ListBox)).call(this, props));
  }

  _createClass(ListBox, [{
    key: 'render',
    value: function render() {
      return React.createElement(
        'div',
        { className: 'col-xl-3 col-md-6 mb-4' },
        React.createElement(
          'div',
          { className: "card border-bottom-" + this.props.accent + " shadow h-100 py-2" },
          this.props.children
        )
      );
    }
  }]);

  return ListBox;
}(React.Component);

var CardBox = function (_React$Component3) {
  _inherits(CardBox, _React$Component3);

  function CardBox(props) {
    _classCallCheck(this, CardBox);

    return _possibleConstructorReturn(this, (CardBox.__proto__ || Object.getPrototypeOf(CardBox)).call(this, props));
  }

  _createClass(CardBox, [{
    key: 'render',
    value: function render() {
      // if (this.state.liked) {
      //   return 'You liked this.';
      // }

      return React.createElement(
        ListBox,
        { accent: 'primary' },
        React.createElement(
          'div',
          { className: 'card-body' },
          React.createElement(
            'span',
            null,
            this.props.card.question
          ),
          React.createElement(
            'span',
            null,
            this.props.card.answer
          )
        )
      );
    }
  }]);

  return CardBox;
}(React.Component);

ReactDOM.render(React.createElement(CardsContainer, null), document.querySelector('#cards_container'));