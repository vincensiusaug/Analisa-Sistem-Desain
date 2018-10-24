import java.sql.*;
import java.util.*;

public class DBReader{

    public DBReader(){
        String url = "jdbc:sqlite:user.db";
        Connection conn = null;
        try {
            conn = DriverManager.getConnection(url);
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }

        String sql = "SELECT id, name, capacity FROM warehouses";
        try{
            Statement stmt  = conn.createStatement();
            ResultSet rs    = stmt.executeQuery(sql);
            while (rs.next()) {
                System.out.println(rs.getInt("Id") +  "\t" + 
                                   rs.getString("Name") + "\t");
            }
        } catch(Exception e){

        }
    }

    public static void main(String[] args) {
        new DBReader();
    }
}