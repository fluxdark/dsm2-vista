/*
    Copyright (C) 1996-2000 State of California, Department of 
    Water Resources.

    VISTA : A VISualization Tool and Analyzer. 
	Version 1.0
	by Nicky Sandhu
    California Dept. of Water Resources
    Division of Planning, Delta Modeling Section
    1416 Ninth Street
    Sacramento, CA 95814
    (916)-653-7552
    nsandhu@water.ca.gov

    Send bug reports to nsandhu@water.ca.gov

    This program is licensed to you under the terms of the GNU General
    Public License, version 2, as published by the Free Software
    Foundation.

    You should have received a copy of the GNU General Public License
    along with this program; if not, contact Dr. Francis Chung, below,
    or the Free Software Foundation, 675 Mass Ave, Cambridge, MA
    02139, USA.

    THIS SOFTWARE AND DOCUMENTATION ARE PROVIDED BY THE CALIFORNIA
    DEPARTMENT OF WATER RESOURCES AND CONTRIBUTORS "AS IS" AND ANY
    EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
    PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE CALIFORNIA
    DEPARTMENT OF WATER RESOURCES OR ITS CONTRIBUTORS BE LIABLE FOR
    ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
    OR SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA OR PROFITS; OR
    BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
    USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
    DAMAGE.

    For more information about VISTA, contact:

    Dr. Francis Chung
    California Dept. of Water Resources
    Division of Planning, Delta Modeling Section
    1416 Ninth Street
    Sacramento, CA  95814
    916-653-5601
    chung@water.ca.gov

    or see our home page: http://wwwdelmod.water.ca.gov/

    Send bug reports to nsandhu@water.ca.gov or call (916)-653-7552

 */
/* (swing1.1) */
package vista.gui;

import java.awt.Component;
import java.awt.Graphics;

import javax.swing.Icon;
import javax.swing.SwingConstants;
import javax.swing.plaf.basic.BasicArrowButton;

/**
 * @version 1.0 02/26/99
 */
public class ArrowIcon implements Icon, SwingConstants {
	private static final int DEFAULT_SIZE = 11;
	// private static final int DEFAULT_SIZE = 5;

	private int size;
	private int iconSize;
	private int direction;
	private boolean isEnabled;
	private BasicArrowButton iconRenderer;

	public ArrowIcon(int direction, boolean isPressedView) {
		this(DEFAULT_SIZE, direction, isPressedView);
	}

	public ArrowIcon(int iconSize, int direction, boolean isEnabled) {
		this.size = iconSize / 2;
		this.iconSize = iconSize;
		this.direction = direction;
		this.isEnabled = isEnabled;
		iconRenderer = new BasicArrowButton(direction);
	}

	public void paintIcon(Component c, Graphics g, int x, int y) {
		iconRenderer.paintTriangle(g, x, y, size, direction, isEnabled);
	}

	public int getIconWidth() {
		// int retCode;
		switch (direction) {
		case NORTH:
		case SOUTH:
			return iconSize;
		case EAST:
		case WEST:
			return size;
		}
		return iconSize;
	}

	public int getIconHeight() {
		switch (direction) {
		case NORTH:
		case SOUTH:
			return size;
		case EAST:
		case WEST:
			return iconSize;
		}
		return size;
	}
}
