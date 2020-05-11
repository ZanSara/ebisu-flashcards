'use strict';

class StudyCard extends React.Component {
  state = {
    card_data: [],
    deck_id: 0 
  }

  componentDidMount() {
    const token = window.localStorage.getItem("token");
    this.state.deck_id = window.location.pathname.split('/').pop();
    fetch('http://127.0.0.1:5000/api/study/'+this.state.deck_id, 
      { method:'GET',
        headers:  new Headers({'Authorization': 'Bearer '+token}),
      })
    .then(res => res.json())
    .then((data) => {
      this.setState({ card_data: data })
    })
    .catch(console.log)
  };

  render() {
    return (
        <div className="col-xl-6 col-lg-5 mx-auto">
          <div className="card shadow mb-4">
            <div className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
              <a href="#" className="btn btn-default btn-sm"><i className="fa fa-chevron-left"></i></a>
              <span className="m-0">Card # -- </span>
              <div className="dropdown no-arrow">
                <a className="dropdown-toggle" href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  <i className="fas fa-ellipsis-v fa-sm fa-fw text-gray-400"></i>
                </a>
                <div className="dropdown-menu dropdown-menu-right shadow animated--fade-in" aria-labelledby="dropdownMenuLink">
                  <a className="dropdown-item" href="#">Skip</a>
                  <a className="dropdown-item" href="#">Mark</a>
                  <a className="dropdown-item" href={"/edit/"+this.state.deck_id}>Edit</a>
                </div>
              </div>
            </div>
            <div className="card-body text-center">
              <div className="row justify-content-center py-3" >
                <div className="col-12 text-center py-3">
                  {this.state.card_data.question}
                </div>
                <div className="col-6 py-3">
                  <input type="text form-control-lg" placeholder="Your answer..." style={{width:100+"%", textAlign:'center'}}/>
                </div>
              </div>
          
              <a id="answerButton" href="#answerArea" className="btn btn-primary" data-toggle="collapse" role="button" 
                  aria-expanded="true" aria-controls="collapseCardExample" onClick="getElementById('answerButton').style.display = 'none'">
                  Click to show answer
              </a>
          
              <div className="collapse hide" id="answerArea">
                  <div className="card-body">
                      <div></div>
                      <div>
                      {this.state.card_data.answer}  
                      </div>
                      <hr />

                      <form action={"api/study/"+this.state.deck_id} method="POST">
                        <button type="submit" name="test_result" value="0" className="btn btn-danger">
                          <i className="fas fa-fw fa-times d-md-none"></i>
                          <span className="d-none d-sm-inline-block">I forgot :(</span>
                        </button>
                        <button type="submit" name="test_result" value="1" className="btn btn-success">
                          <i className="fas fa-fw fa-check d-md-none"></i>
                          <span className="d-none d-sm-inline-block">I remember!</span>
                        </button>
                      </form>
          
                  </div>
              </div>          
            </div>    
          </div>
        </div>
    );
  }
}

ReactDOM.render(
  <StudyCard />,
  document.querySelector('#card_to_study')
);

