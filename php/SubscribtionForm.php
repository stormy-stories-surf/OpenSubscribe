<!DOCTYPE HTML>
<html>
<head>
<style>
.error {color: #FF0000;}
</style>
</head>
<body>

<?php

function check_mail_address($mailAddress_p) {

	// declare local variables
	$errorText_l = "";

	// check if mail is empty
	if (empty($mailAddress_p)) {
		$errorText_l = "<br /> Bitte gebe eine Email-Adresse ein.";
	} else {
		// check if e-mail address is well-formed
		if (!filter_var($mailAddress_p, FILTER_VALIDATE_EMAIL)) {
			$errorText_l = "<br /> Ungültiges Email-Adressen Format";
		}
	}

	// return error text
	return $errorText_l;

}

function cleanupStringFromSpecialCharacters($string_p) {
	// strip unnecessary characters (extra space, tab, newline) from the user input data
	$string_p = trim($string_p);

	// remove backslashes () from the user input data
	$string_p = stripslashes($string_p);

	// converts special characters to HTML entities
	// for example convert < and > into &lt; and &gt;
	$string_p = htmlspecialchars($string_p);

	// return cleaned
	return $string_p;
}

function insert_new_subscriber($mailAddress_p) {
        // open database connection
	$pdo_l = new PDO('mysql:host=localhost;dbname=OpenSubscribe', 'SubscribtionFormUser', '<PUT_YOUR_PASSWORD_HERE>');

	// prepare and execute insert
        $cryptoStrong_l = True;
        $subscribeID_l = openssl_random_pseudo_bytes(64,$cryptoStrong_l);
       	$unsubscribeID_l = openssl_random_pseudo_bytes(64,$cryptoStrong_l);
        $subscribeID_l = bin2hex($subscribeID_l);
       	$unsubscribeID_l = bin2hex($unsubscribeID_l);
	$statement = $pdo_l->prepare("INSERT INTO subscriber(id, mailaddress, subscribeID, unsubscribeID, confirmationMailSent, subscribtionConfirmed) VALUES (NULL, ?, ?, ?, false, false)");
	$statement->execute(array($mailAddress_p, $subscribeID_l, $unsubscribeID_l));
        echo "Inserted new subscriber " . $mailAddress_p . " with subscribeID : " . $subscribeID_l . " and with unsubscribeID : " . $unsubscribeID_l . "<br />";

}

function select_all_subscribers() {
        // open database connection
	$pdo_l = new PDO('mysql:host=localhost;dbname=OpenSubscribe', 'SubscribtionFormUser', '<PUT_YOUR_PASSWORD_HERE>');

	// select and print all from subscriber table
	$sql_l = "SELECT * FROM subscriber";
	foreach ($pdo_l->query($sql_l) as $row_l) {
		echo $row_l['id']."<br />";
		echo $row_l['mailaddress']."<br />";
		echo $row_l['subscribeID']."<br />";
		echo $row_l['unsubscribeID']."<br />";
		echo $row_l['confirmationMailSent']."<br />";
		echo $row_l['subscribtionConfirmed']."<br />";
	}
}

function check_time_since_last_request_okay() {
        // open database connection
	$pdo_l = new PDO('mysql:host=localhost;dbname=OpenSubscribe', 'SubscribtionFormUser', '<PUT_YOUR_PASSWORD_HERE>');

        // get last subscribtion time
	$timeOfLastSubscribtionAsString_l = "1970-01-01 01:01:01";
        $sql_l = "SELECT * FROM lastSubscribtion";

        foreach ($pdo_l->query($sql_l) as $row_l) {
                $timeOfLastSubscribtionAsString_l = $row_l['timeOfLastSubscribtion'];
	}

        $timeOfLastSubscribtion = new DateTime($timeOfLastSubscribtionAsString_l, new DateTimeZone('UTC'));

	// get current time
        $now = new DateTime($now, new DateTimeZone('UTC'));

	echo "<br />";
	echo "check if time since last request is > 5 seconds <br />";
	echo "last subscribtion time " . $timeOfLastSubscribtion->format('Y-m-d H:i:s') . "<br />";
	echo "current time " . $now->format('Y-m-d H:i:s') . "<br />";

	// get difference in seconds
	$diffInSeconds = $now->getTimestamp() - $timeOfLastSubscribtion->getTimestamp();
        echo "difference is " . $diffInSeconds . " seconds <br /> <br />";

	// check if timestamp of last request is more 5 seconds before the timestamp of current request
	if ($diffInSeconds < 5) {
		return false;
	} else {

		// prepare and execute delete all
		$statement = $pdo_l->prepare("DELETE FROM lastSubscribtion");
		$statement->execute();

		// prepare and execute insert
		$statement = $pdo_l->prepare("INSERT INTO lastSubscribtion (id, timeOfLastSubscribtion) VALUES (NULL, ?)");
		$statement->execute(array($now->format('Y-m-d H:i:s')));
		return true;
	}

}

// main
if ($_SERVER["REQUEST_METHOD"] == "POST") {

	// get email address from html
	$email = cleanupStringFromSpecialCharacters($_POST["email"]);

	// check if mail address is well formated
	$errorText = check_mail_address($email);

	if ($errorText == "") {

		// check if time since last request was long enough
		if (check_time_since_last_request_okay()) {
			insert_new_subscriber($email);
			//select_all_subscribers();
			$successText = "Hurra! Du hast dich auf unserer Website angemeldet. <br />" .
			"Schon bald wirst du automatisch per Mail über unsere neuen Beiträge benachrichtigt. <br />" .
			"Aber vorher bestätige bitte noch einmal dein Abonnement. Hierzu findest du eine neue Mail mit einem Aktivierungslink in deinem Posteingang. <br />";
		}
	}

}

?>

<h3>Abonniere unseren Newsletter</h3>
Du willst benachrichtigt werden, wenn wir einen neuen Beitrag veröffentlichen? Dann trage dich hier in unsere Mailing - Liste mit ein :)
<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
  E-mail: <input type="text" name="email" value="<?php echo $email;?>">
  <span class="error">* <?php echo $errorText;?></span>
  <br><br>
  <input type="submit" name="submit" value="Abonnieren!">
</form>

<?php echo $successText;?>
