<?php
	
	function get_course_array($department){
		$db = new PDO('sqlite:example.sqlite3'); 
		$req = 'select * from courses WHERE department_id  = ' . intval($department) ;
		$rs = $db->query($req);
		$retarray = array();
		foreach($rs as $row){
			$retarray[] = $row['id'] . ':' . $row['code'] . " - " . $row['title'];
		}
		return $retarray;
	}
	
	function get_section_array($department, $course){
		$db = new PDO('sqlite:example.sqlite3'); 
		$req = 'select * from sections WHERE course_id  = ' . intval($course);
		$rs = $db->query($req);
		$retarray = array();
		foreach($rs as $row){
			$retarray[] = $row['id'] . ':' . $row['code'] . " - " . $row['reg'] . '/' . $row['seats'] . ' registered';
		}
		return $retarray;
	}

	if (isset($_REQUEST['department'])){
		if (isset($_REQUEST['course']) && $_REQUEST['course'] != 0){
			$sections = get_section_array($_REQUEST['department'], $_REQUEST['course']);
			echo json_encode($sections);
		} else {
			$courses = get_course_array($_REQUEST['department']);
			echo json_encode($courses);
		}
	}else {
		echo "failure";
	}
?>
