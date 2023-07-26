<?php
// get url and clickCounterID from parameters
$encodedUrl = $_GET['data'];
$clickCounterID = $_GET['clickCounterID'];

// decode encoded url parameter
$decodedUrl = urldecode($encodedUrl);

// update_click_counter
// @clickCounterID_p : non-iterateable id which identifies a newsletter mail inside the database table
//
// selects the current value of the click counter for this newsletter mail
// increments the click counter value and updates the database with the
// new value of the click counter
function update_click_counter($clickCounterID_p) {
  // open database connection
	$pdo_l = new PDO('mysql:host=localhost;dbname=OpenSubscribe', 'UpdateClickCounterUser', '<PUT_YOUR_UPDATE_CLICK_COUNTER_USER_PASSWORD_HERE>');

  // get current click counter
  $clickCounter_l = 0;
	$foundClickCounter_l = 0;
  $statement_l = $pdo_l->prepare("SELECT clickCounter FROM newsletter WHERE clickCounterID = ?");
  $statement_l->execute(array($clickCounterID_p));
  while($row_l = $statement_l->fetch()) {
     $clickCounter_l = $row_l['clickCounter'];
		 $foundClickCounter_l = 1;
  }

	// if clickCounterID was found increase it,
	if ($foundClickCounter_l == 1) {
			// increment click counter
		  $clickCounter_l = intval($clickCounter_l) + 1;

			// prepare and execute update of click counter
		  $sql_l = "UPDATE newsletter SET clickCounter=" . $clickCounter_l . " WHERE clickCounterID=?";
		  $pdo_l->prepare($sql_l)->execute([$clickCounterID_p]);
	} else {
		// click-counter id was not found, maybe it is clickCounter2 that you are looking for?
		// try to search for clickCounter2

		// get current click counter
	  $clickCounter2_l = 0;
		$foundClickCounter2_l = 0;
	  $statement2_l = $pdo_l->prepare("SELECT clickCounter2 FROM newsletter WHERE clickCounter2ID = ?");
	  $statement2_l->execute(array($clickCounterID_p));
	  while($row2_l = $statement2_l->fetch()) {
	     $clickCounter2_l = $row2_l['clickCounter2'];
			 $foundClickCounter2_l = 1;
	  }

		// if clickCounterID was found increase it,
		if ($foundClickCounter2_l == 1) {
				// increment click counter
			  $clickCounter2_l = intval($clickCounter2_l) + 1;

				// prepare and execute update of click counter
			  $sql_l = "UPDATE newsletter SET clickCounter2=" . $clickCounter2_l . " WHERE clickCounter2ID=?";
			  $pdo_l->prepare($sql_l)->execute([$clickCounterID_p]);

	}


}

update_click_counter($clickCounterID);

// redirect to decoded url
header("Location: ".$decodedUrl);
?>
