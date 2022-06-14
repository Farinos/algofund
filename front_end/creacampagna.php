<?php
include('res/header.php');
?>
<main id="main">

  <section id="faq" class="faq">

    <div class="container" data-aos="fade-up">

      <header class="section-header">
        <h2>Crea Campagna</h2>
        <p>Inserisci il tuo progetto </p>
      </header>

      <div class="row">

        <form method="post" action="">
          <div class="container">
            <h1 class="display-5 mt-2">Inserisci un nuovo Progetto</h2>

              <div class="row">
                <div class="col-8">
                  <div class="card">
                    <div class="card-body">
                      <div class="row">
                        <div class="col">
                          <input type="text" name="nomeprogetto" class="form-control my-2 w-100" placeholder="Nome Progetto">
                          <input type="text" name="nomeautore" class="form-control my-2 w-100" placeholder="Nome Autore">

                        </div>
                        <div class="col">
                          <select name="categoria" id="categoria" class="form-control w-100 my-2" type="text">
                            <option value=" ">Inserisci Categoria ↓ </option>
                            <option value="raccolte_benefiche"> Raccolte Benefiche</option>
                            <option value="emergenze"> Emergenze</option>
                            <option value="terza_categoria"> Terza Categoria</option>
                          </select>
                          <input type="file" class="form-control-file mt-1" id="exampleFormControlFile1">
                        </div>
                      </div>
                      <textarea class="form-control" id="exampleFormControlTextarea1" rows="3">Descrizione Progetto</textarea>
                      <button type="submit" class="btn btn-primary mt-2" name="nuovoatto">Inserisci</button>
                    </div>
                  </div>
                </div>
                <div class="col">
                  <img src="assets/img/lavoro.png" width="50%">
                </div>
              </div>
        </form>
      </div>
    </div>
  </section>
  <footer id="footer" class="footer">
    <div class="footer-newsletter">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-12 text-center">
            <h4>Our Newsletter</h4>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam in scelerisque lorem. Nulla facilisi. Aliquam finibus mollis velit vel porttitor. Mauris sit amet eros pharetra, luctus purus quis, molestie ante. Nullam rhoncus rutrum erat vitae vestibulum. Quisque in ligula a odio ultricies facilisis.</p>
          </div>
          <div class="col-lg-6">
            <form action="" method="post">
              <input type="email" name="email"><input type="submit" value="Subscribe">
            </form>
          </div>
        </div>
      </div>
    </div>
    <?php
    include('res/footer.php');
    ?>