<?php
	function valid_email($email){
		if (filter_var($email, FILTER_VALIDATE_EMAIL)) {
			return true;
		}
		return false;
	}

	function valid_phone($phone){
		return is_numeric($phone) && strlen($phone) == 10;
	}

	function find_user_id($db, $email){
		$sql = $db->prepare('select user_id from users where email = :email');
		$sql->execute(array(':email'=>$email));
		$ret = $sql->fetchAll();
		return $ret;

	}

	if (isset($_REQUEST['email']) && isset($_REQUEST['phone'])){
		if (!valid_email($_REQUEST['email'])){
			echo 'email0';
			exit();
		}
		$email = $_REQUEST['email'];
		if (!valid_phone($_REQUEST['phone'])){
			echo 'phone0';
			exit();
		}
		$phone = $_REQUEST['phone'];
		$db = new PDO('sqlite:example.sqlite3');
		$ret = find_user_id($db, $email);
		if (count($ret) != 0){
			echo ($ret[0]['user_id']);
		} else {
			$sql = $db->prepare("insert into users (email, username, phone) values (:email, :email, :phone);");
			if (!$sql) {
				echo ($pdo->errorInfo());
			}
			$sql->execute(array(':email' => $email, ':phone' => $phone));
			$ret = find_user_id($db, $email);
			echo ($ret[0]['user_id']);
		}
	}

	if (isset($_REQUEST['department']) && isset($_REQUEST['course']) && isset($_REQUEST['section']) && isset($_REQUEST['user'])){
		
		$sect =  intval($_REQUEST['section']); 
		$user_id = intval($_REQUEST['user']);
		$sql = 'insert into alerts (user_id, section_id, active) values(' . $user_id . ',' . $sect . ', 1);';
		$db = new PDO('sqlite:example.sqlite3');
		try {
			$db->exec($sql);
		} catch (PDOException $e){
			echo "exception: " . $e->getMessage();
		}
		echo '0';
	}
?>
