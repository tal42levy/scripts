<!DOCTYPE html>
<html>
  <head>
    <title>Classer</title>
    <!-- Bootstrap -->
    <link href="css/bootstrap.min.css" rel="stylesheet" media="screen">	
		<script type="text/javascript" src="jquery.min.js"></script>
		<script type="text/javascript" src="menus.js"></script>
		<?php 
			function make_dropdown($sel){
				$db = new PDO('sqlite:example.sqlite3');
				$req = 'select * from ' . $sel . ' order by "code" ASC';
				$rs = $db->query($req);
				foreach($rs as $row){
					$res = $row["code"];
					echo "<option value=\"" . $row['id'] . "\">" . $res . "</option><br>";
				}
			}
		?>
  </head>
  <body>
		<form class="form" id="alert">
			<div class="control-group">
				<input type="text" placeholder="Email" id="email">
				<br>
				<input type="text" placeholder="Phone" id="phone">
				<br>
				<select id="deps">
					<option value="0">Department</option>
					<?php $sel = 'departments'; make_dropdown($sel);?>
				</select>
				<br>
				<select id="courses">
					<option value="0">Course</option>
					<?php $sel = 'courses';?>
				</select>
				<br>
				<select id="sects">
					<option value="0">Section</option>
					<?php $sel = 'sections'; ?>
				</select>
				<br>
				<input id="submit" class='btn btn-large btn-success' type="submit" value="Make My Alert!"/>
			</div>
		</form>
	</body>
</html>
