Yehaaa.. you succesfully subscribed to our e-mail newsletter!
<?php

function interpolateQuery($query, $params) {
    echo "params " . $params . "<br/ >";
    $keys = array();

    # build a regular expression for each parameter
    foreach ($params as $key => $value) {
        if (is_string($key)) {
            $keys[] = '/:'.$key.'/';
        } else {
            $keys[] = '/[?]/';
        }
    }

    $query = preg_replace($keys, $params, $query, 1, $count);

    #trigger_error('replaced '.$count.' keys');

    return $query;
}

function update_subscribtion_confirmed($subscribeID_p) {
        // open database connection
	$pdo_l = new PDO('mysql:host=localhost;dbname=OpenSubscribe', 'ConfirmSubscribtionUser', '<PUT_YOUR_CONFIRM_SUBSCRIBTION_USER_PASSWORD_HERE>');

	// prepare and execute insert
	//$statement = $pdo_l->prepare("UPDATE subscriber SET subscribtionConfirmed = true WHERE subscribeID = '?'");
  $sql_l = "UPDATE subscriber SET subscribtionConfirmed=true WHERE subscribeID=?";
  $pdo_l->prepare($sql_l)->execute([$subscribeID_p]);

	//$statement = $pdo_l->prepare("UPDATE subscriber SET subscribtionConfirmed=true WHERE subscribeID='1'");
	//$statement->execute(array($subscribeID_l));

	echo "Updated newsletter subscribtion with subscribeID " . $subscribeID_l . "<br />";
}

// main
if ($_GET["data"] != "") {
	$subscribtionID = $_GET["data"];
        echo "ID is " . $subscribtionID . "<br />";
	update_subscribtion_confirmed($subscribtionID);
}


?>
