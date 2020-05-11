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

      var token = window.localStorage.getItem("token");
      this.state.deck_id = window.location.pathname.split('/').pop();
      fetch('http://127.0.0.1:5000/api/decks/' + this.state.deck_id + "/cards", { method: 'GET',
        headers: new Headers({ 'Authorization': 'Bearer ' + token })
      }).then(function (res) {
        return res.json();
      }).then(function (data) {
        _this2.setState({ cards_data: data });
      }).catch(console.log);
    }
  }, {
    key: 'render',
    value: function render() {
      var _this3 = this;

      var cards = [];
      this.state.cards_data.forEach(function (card) {
        cards.push(React.createElement(CardBox, { card: card, deck_id: _this3.state.deck_id }));
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

var CardWithSidebar = function (_React$Component2) {
  _inherits(CardWithSidebar, _React$Component2);

  function CardWithSidebar(props) {
    _classCallCheck(this, CardWithSidebar);

    return _possibleConstructorReturn(this, (CardWithSidebar.__proto__ || Object.getPrototypeOf(CardWithSidebar)).call(this, props));
  }

  _createClass(CardWithSidebar, [{
    key: 'render',
    value: function render() {
      return React.createElement(
        'div',
        { className: 'col-xl-3 col-lg-4 col-md-6 col-sm-6 col-xs-12 py-2' },
        React.createElement(
          'div',
          { className: "card border-bottom-" + this.props.accent + " bg-gradient-" + this.props.accent + " shadow", style: { flexDirection: 'row' } },
          React.createElement(
            'div',
            { className: 'card-body text-center', style: { width: 3 + "em", maxWidth: 3 + "em", minWidth: 3 + "em", padding: 1 + "rem", lineHeight: 2 + "rem" } },
            React.createElement(
              'a',
              { href: "/api/decks/" + this.props.deck_id + "/cards/" + this.props.card._id.$oid, style: { color: '#fff' } },
              React.createElement('i', { className: 'fas fa-fw fa-pen' })
            ),
            React.createElement(
              'a',
              { href: "/api/decks/" + this.props.deck_id + "/cards/" + this.props.card._id.$oid, onClick: 'return confirm(\'Are you sure you want to delete this card?\')', style: { color: '#fff' } },
              React.createElement('i', { className: 'fas fa-fw fa-trash' })
            )
          ),
          React.createElement(
            'div',
            { className: 'card', style: { width: 100 + "%" } },
            this.props.children
          )
        )
      );
    }
  }]);

  return CardWithSidebar;
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
      return React.createElement(
        CardWithSidebar,
        { card: this.props.card, deck_id: this.props.deck_id, accent: 'primary' },
        React.createElement(
          'div',
          { className: 'card-body text-center' },
          React.createElement(
            'div',
            { className: 'row justify-content-center' },
            React.createElement(
              'div',
              { className: 'col-12 text-center' },
              this.props.card.question,
              React.createElement('hr', null)
            ),
            React.createElement(
              'div',
              { className: 'col-12 text-center' },
              this.props.card.answer
            )
          )
        ),
        React.createElement(
          'div',
          { className: 'card-footer' },
          React.createElement(
            'p',
            null,
            'Last Review: --'
          )
        )
      );
    }
  }]);

  return CardBox;
}(React.Component);

ReactDOM.render(React.createElement(CardsContainer, null), document.querySelector('#cards_container'));