'use strict';

class CardsContainer extends React.Component {
  state = {
    cards_data: [],
    deck_id: 0
  }

  componentDidMount() {
    const token = window.localStorage.getItem("token");
    this.state.deck_id = window.location.pathname.split('/').pop();
    fetch('http://127.0.0.1:5000/api/decks/'+this.state.deck_id+"/cards", 
      { method:'GET',
        headers:  new Headers({'Authorization': 'Bearer '+token}),
      })
    .then(res => res.json())
    .then((data) => {
      this.setState({ cards_data: data })
    })
    .catch(console.log)
  };

  render() {
    const cards = [];
    this.state.cards_data.forEach((card) => {
      cards.push(
        <CardBox card={card} deck_id={this.state.deck_id}/>
      );
    });
    return (
      <div className="row">
        {cards}
      </div>
    );
  }
}


class CardWithSidebar extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div className="col-xl-3 col-lg-4 col-md-6 col-sm-6 col-xs-12 py-2">
        <div className={"card border-bottom-"+this.props.accent +" bg-gradient-"+this.props.accent +" shadow"} style={{flexDirection: 'row'}}>
            <div className="card-body text-center" style={{width: 3+"em", maxWidth:3+"em", minWidth: 3+"em", padding:1+"rem", lineHeight:2+"rem"}}>
            <a href={"/api/decks/"+this.props.deck_id+"/cards/"+this.props.card._id.$oid} style={{color:'#fff'}}>
                <i className="fas fa-fw fa-pen"></i>
            </a>
            <a href={"/api/decks/"+this.props.deck_id+"/cards/"+this.props.card._id.$oid} onClick="return confirm('Are you sure you want to delete this card?')" style={{color: '#fff'}}>
                <i className="fas fa-fw fa-trash"></i>
            </a>
            </div>
            <div className="card" style={{width:100+"%"}}>
                {this.props.children}
            </div>
        </div>
      </div>
    );
  }
}


class CardBox extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
        <CardWithSidebar card={this.props.card} deck_id={this.props.deck_id} accent="primary">
          <div className="card-body text-center">
            <div className="row justify-content-center">
              <div className="col-12 text-center">
                {this.props.card.question}
              <hr />
              </div>
              <div className="col-12 text-center">
                {this.props.card.answer}
              </div>
            </div>
          </div>
          <div className="card-footer">
            <p>Last Review: --</p>
          </div>
        </CardWithSidebar>
    );
  }
}

ReactDOM.render(
  <CardsContainer />,
  document.querySelector('#cards_container')
);

