'use strict';

class StudyCard extends React.Component {
  state = {
    card_data: []
  }

  componentDidMount() {
    const deck_id = window.location.pathname.split('/').pop();
    console.log("PATH :  " + deck_id);
    fetch('http://127.0.0.1:5000/api/study/'+deck_id, 
      { method:'GET',
        headers:  new Headers({'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODgwOTY3MjQsIm5iZiI6MTU4ODA5NjcyNCwianRpIjoiMjY4ZjQ2MDAtNzFhZC00ZTY1LThhNjAtZTZjYzM1MmIwYzdhIiwiZXhwIjoxNTg4NzAxNTI0LCJpZGVudGl0eSI6IjVlYTQyMzMyOWM1YWZjNjA4MjBlYzA4MSIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.73vHmWLDkeBVtflBVMKc-FKOY594V8z0nQ8qqsM8OyA'}),
      })
    .then(res => res.json())
    .then((data) => {
      this.setState({ card_data: data });
      console.log("CARD DATA:  " + card_data);
    })
    .catch(console.log)
  };

  render() {
    return (
      <div className="row">
        <div class="col-xl-6 col-lg-5 mx-auto">
          <div class="card shadow mb-4">
            <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
              <a href="#" class="btn btn-default btn-sm"><i class="fa fa-chevron-left"></i></a>
              <span class="m-0">Card # -- </span>
              <div class="dropdown no-arrow">
                <a class="dropdown-toggle" href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  <i class="fas fa-ellipsis-v fa-sm fa-fw text-gray-400"></i>
                </a>
                <div class="dropdown-menu dropdown-menu-right shadow animated--fade-in" aria-labelledby="dropdownMenuLink">
                  <a class="dropdown-item" href="#">Modify Card</a>
                  <a class="dropdown-item" href="#">Skip Card</a>
                  <div class="dropdown-divider"></div>
                  <a class="dropdown-item" href="#">Something else</a>
                </div>
              </div>
            </div>
            <div class="card-body text-center">
              <div class="row justify-content-center py-3" >
                <div class="col-12 text-center py-3">
                  {this.state.card_data.question}
                </div>
                <div class="col-6 py-3">
                  <input type="text form-control-lg" placeholder="Your answer..." style="width:100%;"/>
                </div>
              </div>
          
              <a id="answerButton" href="#answerArea" class="btn btn-primary" data-toggle="collapse" role="button" 
                  aria-expanded="true" aria-controls="collapseCardExample" onclick="getElementById('answerButton').style.display = 'none';">
                  Click to show answer
              </a>
          
              <div class="collapse hide" id="answerArea">
                  <div class="card-body">
                      <div></div>
                      <div>
                      {this.state.card_data.answer}  
                      </div>
                      <hr />

                      <form method="POST">
                        <button type="submit" name="test_result" value="0" class="btn btn-danger" type="button">
                          <i class="fas fa-fw fa-times d-md-none"></i>
                          <span class="d-none d-sm-inline-block">I forgot :(</span>
                        </button>
                        <button type="submit" name="test_result" value="1" class="btn btn-success" type="button">
                          <i class="fas fa-fw fa-check d-md-none"></i>
                          <span class="d-none d-sm-inline-block">I remember!</span>
                        </button>
                      </form>
          
                  </div>
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
  document.querySelector('#card_container')
);

