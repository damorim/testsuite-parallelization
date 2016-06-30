package br.ufpe.cin.dchecker;

import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.HashSet;
import java.util.Scanner;
import java.util.Set;

import br.ufpe.cin.dchecker.core.DependencyAnalyzer;
import br.ufpe.cin.dchecker.model.CheckableInfo;
import br.ufpe.cin.dchecker.model.TestRunInfo;

/**
 *
 * @author Jeanderson Candido <http://jeandersonbc.github.io>
 *
 */
public class Main {

	public static void main(String[] args) throws FileNotFoundException {
		String path = args[0];
		DependencyAnalyzer.check(entriesFromFile(path));
	}

	private static Set<CheckableInfo> entriesFromFile(String path) throws FileNotFoundException {
		Scanner sc = new Scanner(new BufferedInputStream(new FileInputStream(path)));

		// Parse and load all entries in memory
		Set<CheckableInfo> entriesFromFile = new HashSet<>();
		while (sc.hasNext()) {
			entriesFromFile.add(TestRunInfo.parseRunningInfo(sc.nextLine()));
		}
		sc.close();

		return entriesFromFile;
	}
}
