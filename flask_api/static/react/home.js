'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var DecksContainer = function (_React$Component) {
  _inherits(DecksContainer, _React$Component);

  function DecksContainer() {
    var _ref;

    var _temp, _this, _ret;

    _classCallCheck(this, DecksContainer);

    for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }

    return _ret = (_temp = (_this = _possibleConstructorReturn(this, (_ref = DecksContainer.__proto__ || Object.getPrototypeOf(DecksContainer)).call.apply(_ref, [this].concat(args))), _this), _this.state = {
      decks_data: []
    }, _temp), _possibleConstructorReturn(_this, _ret);
  }

  _createClass(DecksContainer, [{
    key: 'componentDidMount',
    value: function componentDidMount() {
      var _this2 = this;

      var token = window.localStorage.getItem("token");
      console.log(token);
      fetch('http://127.0.0.1:5000/api/decks', { method: 'GET',
        headers: new Headers({ 'Authorization': 'Bearer ' + token })
      }).then(function (res) {
        return res.json();
      }).then(function (data) {
        _this2.setState({ decks_data: data });
      }).catch(console.log);
    }
  }, {
    key: 'render',
    value: function render() {
      var decks = [];
      this.state.decks_data.forEach(function (deck) {
        decks.push(React.createElement(DeckCard, { deck: deck }));
      });
      return React.createElement(
        'div',
        { className: 'row' },
        decks
      );
    }
  }]);

  return DecksContainer;
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

var EditDropdown = function (_React$Component3) {
  _inherits(EditDropdown, _React$Component3);

  function EditDropdown(props) {
    _classCallCheck(this, EditDropdown);

    return _possibleConstructorReturn(this, (EditDropdown.__proto__ || Object.getPrototypeOf(EditDropdown)).call(this, props));
  }

  _createClass(EditDropdown, [{
    key: 'render',
    value: function render() {
      return React.createElement(
        'div',
        { className: 'dropdown no-arrow' },
        React.createElement(
          'a',
          { className: 'dropdown-toggle', href: '#', role: 'button', id: 'dropdownMenuLink', 'data-toggle': 'dropdown', 'aria-haspopup': 'true', 'aria-expanded': 'false' },
          React.createElement(
            'h5',
            { className: 'text-secondary' },
            React.createElement('i', { className: 'fas fa-fw fa-pen text-gray-500' })
          )
        ),
        React.createElement(
          'div',
          { className: 'dropdown-menu dropdown-menu-right shadow animated--fade-in', 'aria-labelledby': 'dropdownMenuLink' },
          this.props.children
        )
      );
    }
  }]);

  return EditDropdown;
}(React.Component);

var DeckCard = function (_React$Component4) {
  _inherits(DeckCard, _React$Component4);

  function DeckCard(props) {
    _classCallCheck(this, DeckCard);

    return _possibleConstructorReturn(this, (DeckCard.__proto__ || Object.getPrototypeOf(DeckCard)).call(this, props));
  }

  _createClass(DeckCard, [{
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
            'div',
            { className: 'd-flex flex-row align-items-center justify-content-between' },
            React.createElement(
              'h1',
              { className: 'text-primary' },
              React.createElement(
                'a',
                { href: "study/" + this.props.deck._id.$oid },
                this.props.deck.name
              )
            ),
            React.createElement(
              EditDropdown,
              null,
              React.createElement(
                'a',
                { href: "edit/" + this.props.deck._id.$oid, className: 'dropdown-item btn' },
                'Edit Deck'
              ),
              React.createElement(
                'a',
                { href: "edit/" + this.props.deck._id.$oid, className: 'dropdown-item btn' },
                'Cards List'
              )
            )
          ),
          React.createElement(
            'span',
            null,
            this.props.deck.description
          )
        ),
        React.createElement(
          'div',
          { className: 'card-footer' },
          'Cards to review: ',
          this.props.deck.cards_to_review,
          React.createElement('br', null),
          'Unknown cards: ',
          this.props.deck.new_cards
        )
      );
    }
  }]);

  return DeckCard;
}(React.Component);

ReactDOM.render(React.createElement(DecksContainer, null), document.querySelector('#decks_container'));