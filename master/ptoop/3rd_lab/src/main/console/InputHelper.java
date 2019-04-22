package main.console;

import java.util.Scanner;

public class InputHelper {
    public static String enterString(String help) {
        System.out.print(help);
        Scanner scanner = new Scanner(System.in);

        return scanner.nextLine();
    }

    public static int enterInt(String help) {
        System.out.print(help);
        Scanner scanner = new Scanner(System.in);

        try {
            return scanner.nextInt();
        } catch (Exception e) {
            System.out.println("Error: Invalid option.");
            return -Integer.MAX_VALUE;
        }
    }
}
