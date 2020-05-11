'use strict';

class DecksContainer extends React.Component {
  state = {
    decks_data: []
  }

  componentDidMount() {
    const token = window.localStorage.getItem("token");
    console.log(token);
    fetch('http://127.0.0.1:5000/api/decks', 
      { method:'GET',
        headers:  new Headers({'Authorization': 'Bearer '+token}),
      })
    .then(res => res.json())
    .then((data) => {
      this.setState({ decks_data: data })
    })
    .catch(console.log)
  };

  render() {
    const decks = [];
    this.state.decks_data.forEach((deck) => {
      decks.push(
        <DeckCard deck={deck} />
      );
    });
    return (
      <div className="row">
        {decks}
      </div>
    );
  }
}


class ListBox extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div className="col-xl-3 col-md-6 mb-4">
        <div className={"card border-bottom-"+this.props.accent +" shadow h-100 py-2"}>
          {this.props.children}
        </div>
      </div>
    );
  }
}

class EditDropdown extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div className="dropdown no-arrow">
      <a className="dropdown-toggle" href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
        <h5 className="text-secondary"><i className="fas fa-fw fa-pen text-gray-500"></i></h5>
      </a>
      <div className="dropdown-menu dropdown-menu-right shadow animated--fade-in" aria-labelledby="dropdownMenuLink">
        {this.props.children}
      </div>
    </div>
    );
  }
}


class DeckCard extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    // if (this.state.liked) {
    //   return 'You liked this.';
    // }

    return (
      <ListBox accent="primary">
        <div className="card-body">
            <div className="d-flex flex-row align-items-center justify-content-between">
              <h1 className="text-primary">
                <a href={"study/" + this.props.deck._id.$oid}>{this.props.deck.name}</a>
              </h1>
              <EditDropdown>
                  <a href={"edit/"+this.props.deck._id.$oid} className="dropdown-item btn">Edit Deck</a>
                  <a href={"edit/"+this.props.deck._id.$oid} className="dropdown-item btn">Cards List</a>
              </EditDropdown>
            </div>
            <span>{this.props.deck.description}</span>
        </div>
        <div className="card-footer">
            Cards to review: {this.props.deck.cards_to_review}
            <br />
            Unknown cards: {this.props.deck.new_cards}
        </div>
      </ListBox>
    );
  }
}

ReactDOM.render(
  <DecksContainer />,
  document.querySelector('#decks_container')
);

